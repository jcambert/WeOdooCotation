from odoo.exceptions import AccessError, UserError
from odoo import models, fields, api, _
from .models import Model

DOMAIN_SALE=('sale_ok', '=', True)
class WeCotationOrder(Model):
    _name='we.cotation.order'
    _description='Quotation order'
    _inherit=['mail.activity.mixin','mail.thread']
    _order='number desc'
    _check_company_auto = True
    _sql_constraints = [
        ('we_cotation_order_uniq', 'unique (number,revision)', "The number/revision already exist!"),
    ]

    @api.model
    def default_get(self, fields):
        defaults = super(WeCotationOrder, self).default_get(fields)
        defaults['deviser_id']=self.env.user
        return defaults
    
    @api.model
    def _default_note(self):
        return self.env['ir.config_parameter'].sudo().get_param('account.use_invoice_terms') and self.env.company.invoice_terms or ''

    active = fields.Boolean(default=True)
    number = fields.Integer('Number',required=True, index=True, tracking=True,copy=False)
    revision = fields.Integer('Revision',default=0, index=True, tracking=True,copy=False)
    # bom_ids = fields.One2many('mrp.bom','quotation_id',string='Boms')
    deviser_id=fields.Many2one('res.users','Deviseur',ondelete='set null',help="Deviseur")
    responsable_id=fields.Many2one('res.users','Responsable',ondelete='set null',help="Responsable")
    stage_id=fields.Many2one('we.cotation.stage',
        ondelete='restrict',
        help="Stage",
        compute='_compute_stage_id',
        group_expand='_read_group_stage_names',
        index=True, tracking=True,copy=False,readonly=False, store=True
        )
    color = fields.Integer('Couleur')
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    note = fields.Text('Terms and conditions', default=_default_note)
    pricelist_id = fields.Many2one(
        'product.pricelist', string='Pricelist', check_company=True,  # Unrequired company
        required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", tracking=1,
        help="If you change the pricelist, only newly added lines will be affected.")
    currency_id = fields.Many2one(related='pricelist_id.currency_id', depends=["pricelist_id"], store=True)
    quotation_lines = fields.One2many('we.cotation.order.line', 'quotation_id', string='Quotation Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)

    show_update_pricelist = fields.Boolean(string='Has Pricelist Changed',
                                           help="Technical Field, True if the pricelist was changed;\n"
                                                " this will then display a recomputation button")
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all', tracking=4)

    @api.onchange('pricelist_id')
    def _onchange_pricelist_id(self):
        if self.quotation_lines and self.pricelist_id and self._origin.pricelist_id != self.pricelist_id:
            self.show_update_pricelist = True
        else:
            self.show_update_pricelist = False
    def update_prices(self):
        self.ensure_one()
        # @see sale.sale line 454
        # lines_to_update = []
        # for line in self.order_line.filtered(lambda line: not line.display_type):
        #     product = line.product_id.with_context(
        #         partner=self.partner_id,
        #         quantity=line.product_uom_qty,
        #         date=self.date_order,
        #         pricelist=self.pricelist_id.id,
        #         uom=line.product_uom.id
        #     )
        #     price_unit = self.env['account.tax']._fix_tax_included_price_company(
        #         line._get_display_price(product), line.product_id.taxes_id, line.tax_id, line.company_id)
        #     if self.pricelist_id.discount_policy == 'without_discount' and price_unit:
        #         discount = max(0, (price_unit - product.price) * 100 / price_unit)
        #     else:
        #         discount = 0
        #     lines_to_update.append((1, line.id, {'price_unit': price_unit, 'discount': discount}))
        # self.update({'order_line': lines_to_update})
        self.show_update_pricelist = False
        self.message_post(body=_("Product prices have been recomputed according to pricelist <b>%s<b> ", self.pricelist_id.display_name))


    def name_get(self):
        return [(record.id, '%s Révision:%s' % (record.number, record.revision ) ) if record.revision else (record.id, record.number) for record in self]

    

    def _read_group_stage_names(self, stages, domain, order):
        search_domain=[]
        stages_ids = stages.search(search_domain)
        return stages_ids

    def _compute_stage_id(self):
        for record in self.filtered(lambda r: not r.stage_id):
            record.stage_id = record._stage_find(domain=[('fold', '=', False)]).id

    @api.depends('quotation_lines.price_subtotal')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount = 0.0
            for line in order.quotation_lines:
                amount += line.price_subtotal
            order.update({
                'amount_total': amount
            })

class WeCotationOrderLine(models.Model):
    _name='we.cotation.order.line'
    _description='Quotation order line'
    _order = 'quotation_id, sequence, id'
    _check_company_auto = True

    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Text(string='Description', required=True)
    currency_id = fields.Many2one(related='quotation_id.currency_id', depends=['quotation_id.currency_id'], store=True, string='Currency', readonly=True)
    company_id = fields.Many2one(related='quotation_id.company_id', string='Company', store=True, readonly=True, index=True)
    quotation_id = fields.Many2one('we.cotation.order', string='Quotation Reference', required=True, ondelete='cascade', index=True, copy=False)
    quotation_number = fields.Char(related='quotation_id.display_name',string='Number',readonly=True)
    # quotation_revision = fields.Many2one(related='quotation_id.revision',string='Revision',store=True,readonly=True,index=True)
    product_id = fields.Many2one('product.product', string='Product', domain="[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]", change_default=True, ondelete='restrict', check_company=True)  # Unrequired company
    product_template_id = fields.Many2one('product.template', string='Product Template',related="product_id.product_tmpl_id", domain=[DOMAIN_SALE])
    product_bom = fields.Many2one('mrp.bom',string='Bom',required=True,domain="[('product_tmpl_id','=',product_template_id)]")
    product_updatable = fields.Boolean(compute='_compute_product_updatable', string='Can Edit Product', readonly=True, default=True)
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    product_uom_readonly = fields.Boolean(compute='_compute_product_uom_readonly')

    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0)
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    state = fields.Selection(related='quotation_id.state', string='Quotation Status', readonly=True, copy=False, store=True, default='draft')
    
    @api.depends('product_id', 'quotation_id.state')
    def _compute_product_updatable(self):
        for line in self:
            if line.state in ['done', 'cancel'] :
                line.product_updatable = False
            else:
                line.product_updatable = True
    @api.depends('state')
    def _compute_product_uom_readonly(self):
        for line in self:
            line.product_uom_readonly = line.state in ['sale', 'done', 'cancel']
    
    @api.depends('product_uom_qty', 'discount', 'price_unit')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            subtotal = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            line.update({
                'price_subtotal': subtotal,
            })
    @api.onchange('product_bom')
    def _on_product_bom_changed(self):
        for line in self.filtered(lambda r:r.product_template_id):
            line.price_unit = line._get_price_from_bom()

    @api.model
    def _get_price_from_bom(self, boms_to_recompute=False):
        self.ensure_one()
        bom = self.env['mrp.bom']._bom_find(product_tmpl=self.product_template_id)
        return  self._compute_bom_price(bom, boms_to_recompute=boms_to_recompute) if bom else 0.0

    
    def _compute_bom_price(self, bom, boms_to_recompute=False):
        self.ensure_one()
        if not bom:
            return 0
        if not boms_to_recompute:
            boms_to_recompute = []
        total = 0
        for opt in bom.operation_ids:
            duration_expected = (
                opt.workcenter_id.time_start +
                opt.workcenter_id.time_stop +
                opt.time_cycle)
            total += (duration_expected / 60) * opt.workcenter_id.costs_hour
        for line in bom.bom_line_ids:
            if line._skip_bom_line(self):
                continue

            # Compute recursive if line has `child_line_ids`
            if line.child_bom_id and line.child_bom_id in boms_to_recompute:
                child_total = line.product_id._compute_bom_price(line.child_bom_id, boms_to_recompute=boms_to_recompute)
                total += line.product_id.uom_id._compute_price(child_total, line.product_uom_id) * line.product_qty
            else:
                total += line.product_id.uom_id._compute_price(line.product_id.standard_price, line.product_uom_id) * line.product_qty
        return bom.product_uom_id._compute_price(total / bom.product_qty, self.product_uom)