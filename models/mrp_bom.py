from odoo.exceptions import AccessError, UserError, ValidationError
from odoo import models, fields, api, _
from .models import Model
from .res_config_settings import DIMENSION_ATTRIBUTE, UOM_SURFACE, UOM_WEIGHT, UOM_LENGTH, UOM_VOLUMIC_MASS
class WeBom(Model):
    _inherit='mrp.bom'

    type = fields.Selection(selection_add=[('quot','Quotation')], ondelete={'quot': 'cascade'})
    quotation_line_ids = fields.One2many('we.cotation.order.line','product_bom',string='Quotation Lines')
    
    @api.model
    def _bom_find(self, product_tmpl=None, product=None, picking_type=None, company_id=False, bom_type=False):
        """ Finds BoM for particular product, picking and company """
        if product and product.type == 'service' or product_tmpl and product_tmpl.type == 'service':
            return self.env['mrp.bom']
        domain = self._bom_find_domain(product_tmpl=product_tmpl, product=product, picking_type=picking_type, company_id=company_id, bom_type=bom_type)
        if domain is False:
            return self.env['mrp.bom']
        if not bom_type:
            domain+=[('type', '!=', 'quot')]
        return self.search(domain, order='sequence, product_id', limit=1)

    @api.constrains('type')
    def check_type(self) :
        for record in self:
            if record._origin.type=='quot' and record.quotation_line_ids.search_count([])>0:
                raise ValidationError(_('The type must be Quotation when a calculation is linked to'))
        

class WeBomLine(Model):
    _inherit = 'mrp.bom.line'

    calculation_ids = fields.One2many('we.cotation.bom.line.calculation', 'bom_line_id', 'Calculations', required=True)
    calculation_id = fields.Many2one('we.cotation.bom.line.calculation', 'Calculation', compute='_compute_calculation_id')
    is_calculation =fields.Boolean(string='is calculation',compute='_compute_is_calculation')
    has_calculation = fields.Boolean('Has Calculation',compute='_compute_calculation_id')
    

    
    def default_get(self,vals):
        res = super().default_get(vals)
        return res

    def create_calculation(self,log_warning=False):
        self.ensure_one()

        Calculation = self.env['we.cotation.bom.line.calculation']
        values=Calculation.sudo().create_sample()
        values['bom_line_id']=self.id
        calc= Calculation.sudo().create(values)
        return calc

    @api.depends('bom_id.type')
    def _compute_is_calculation(self):
        for record in self:
            record.is_calculation = record.bom_id.type=='quot'

    @api.depends('calculation_ids')
    def _compute_calculation_id(self):
        for record in self:
            record.calculation_id = record.calculation_ids[:1].id
            record.has_calculation=record.calculation_ids.search_count([])>0


    def edit_calculation_action(self):
        print('edit calculation action')
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("WeOdooCotation.we_cotation_bom_line_calculation_action")
        action['res_id'] =self.env['we.cotation.bom.line.calculation'].search([('bom_line_id','=',self.id)],limit=1).id
        action['views'] = [(self.env.ref('WeOdooCotation.we_cotation_bom_line_calculation_view_form').id, 'form')]
        return action

    def create_calculation_action(self):
        self.ensure_one()
        print('create calculation action')
        action = self.env["ir.actions.actions"]._for_xml_id("WeOdooCotation.we_cotation_bom_line_calculation_action")
        action['res_id'] =self.create_calculation().id
        action['views'] = [(self.env.ref('WeOdooCotation.we_cotation_bom_line_calculation_view_form').id, 'form')]
        return action
