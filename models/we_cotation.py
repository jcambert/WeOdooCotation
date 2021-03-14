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
    politic_id = fields.Many2one('we.cotation.politic.partner',string='Politic',check_company=True,
        required=True,readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id),('partner_id','=',partner_id)]", tracking=1,
        help="If you change the politic, only newly added lines will be affected.")
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

class WeCotationOrderLine(Model):
    _name='we.cotation.order.line'
    _description='Quotation order line'
    _order = 'quotation_id, sequence, id'
    _check_company_auto = True
    _models={'categs':'we.cotation.order.line.category','uom':'uom.uom'}
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Text(string='Description', required=True)
    currency_id = fields.Many2one(related='quotation_id.currency_id', depends=['quotation_id.currency_id'], store=True, string='Currency', readonly=True)
    company_id = fields.Many2one(related='quotation_id.company_id', string='Company', store=True, readonly=True, index=True)
    quotation_id = fields.Many2one('we.cotation.order', string='Quotation Reference', required=True, on_delete='cascade', index=True, copy=False)
    quotation_number = fields.Char(related='quotation_id.display_name',string='Number',readonly=True)
    categories= fields.One2many('we.cotation.order.line.category','order_line',string='Order Line',on_delete='cascade')
    # quotation_revision = fields.Many2one(related='quotation_id.revision',string='Revision',store=True,readonly=True,index=True)
    product_id = fields.Many2one('product.product', string='Product', domain="[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]", change_default=True, ondelete='restrict', check_company=True)  # Unrequired company
    product_template_id = fields.Many2one('product.template', string='Product Template',related="product_id.product_tmpl_id", domain=[DOMAIN_SALE])
    product_bom = fields.Many2one('mrp.bom',string='Bom',required=True,domain="[('product_tmpl_id','=',product_template_id),('type','=','quot')]")
    product_updatable = fields.Boolean(compute='_compute_product_updatable', string='Can Edit Product', readonly=True, default=True)
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    product_uom = fields.Many2one(_models['uom'] , string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    product_uom_readonly = fields.Boolean(compute='_compute_product_uom_readonly')

    quot_prep_price=fields.Float('Preparation',related='product_template_id.quot_prep_price')
    quot_mo_price=fields.Float('Main Oeuvre',related='product_template_id.quot_mo_price')
    
    price_unit = fields.Float('Unit Price', compute="_compute_price_unit",store=True, digits='Product Price', default=0.0)
    discount = fields.Float(string='Discount (%)', digits='Discount', default=0.0)
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    state = fields.Selection(related='quotation_id.state', string='Quotation Status', readonly=True, copy=False, store=True, default='draft')

    def _get_default_product_uom(self):
        return self.env['uom.uom'].search([], limit=1, order='id').id

    def edit_order_line_action(self):
        self.ensure_one()
        print('Edit order line %s' % self.id)
        action = self.env["ir.actions.actions"]._for_xml_id("WeOdooCotation.we_cotation_order_line_action")
        action['res_id'] =self.id
        action['views'] = [(self.env.ref('WeOdooCotation.we_cotation_order_line_form_view').id, 'form')]
        return action

    def update_price_action(self):
        self.ensure_one()
        self.update_price(update_categories=True)
        
    def name_get(self):
        return [(record.id, '%s x %s %s' % (record.name, record.product_uom_qty,record.product_uom.display_name ) ) for record in self]

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
                'price_subtotal': subtotal * line.product_uom_qty
            })

    # @api.onchange('product_bom')
    # def _on_product_bom_changed(self):
    #     for line in self.filtered(lambda r:r.product_template_id):
    #         line.product_id._set_quotation_price_from_bom(line.product_bom)

    # @api.onchange('product_id')

    @api.depends('categories.marged_price','categories.category','product_uom_qty','product_bom')
    def _compute_price_unit(self):
        for line in self:
            line.update_price()

    @api.model
    def update_price(self, update_categories=False):
        self.ensure_one()
        if update_categories:
            self.update_categories()
        cat_price=0.0
        for cat in self.categories.mapped(lambda r:r.marged_price):
            cat_price+=cat
        self.product_id._set_quotation_price_from_bom(self.product_bom)
        price = (self.product_template_id.quot_prep_price/self.product_uom_qty)+self.product_template_id.quot_mo_price+cat_price
        self.price_unit=price
    @api.model
    def create_categories(self):
        self.ensure_one()
        self.categories=[(5,0,0)]
        def init_categories(line):
            return dict.fromkeys(line.quotation_id.politic_id.categories.category.mapped('id'),0.0)
        new_categ_lines_ids=[]
        categories=init_categories(self)
        self.product_id._set_quotation_categories_from_bom(self.product_bom,categories)

        for key in categories:
            politic_lines=self.quotation_id.politic_id.categories.filtered(lambda r:r.category.id==key)
            for politic_line in politic_lines:
                new_categ_line=self.categs.create({'order_line':self.id, 'category':politic_line.id,'price':categories[key]})
                new_categ_lines_ids.append(new_categ_line.id)
        self.categories=[(6,0,new_categ_lines_ids)]

    @api.model
    def update_categories(self):
        self.ensure_one()
        categories = dict.fromkeys( self.categories.category.category.mapped('id'),0.0)
        self.product_id._set_quotation_categories_from_bom(self.product_bom, categories)
        for cat in categories:
            category=self.categories.filtered(lambda r:r.category.category.id==cat)
            if not category:
                continue
            category.write({'price':categories[cat]})
            
    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines:
            line.create_categories()
        
        return lines