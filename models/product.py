from odoo import models, fields,tools, api,_
from odoo.exceptions import AccessError, UserError,ValidationError
from .res_config_settings import PRODUCT_NAME_FORCE_UPPERCASE
class Product(models.Model):
    _inherit = ['product.template']
    _description = 'Product Quotation Extensions'

    quot_count = fields.Integer('Quotation',compute='_compute_bom_count', compute_sudo=False)
   
    def _compute_quotation_count(self):
        for record in self:
            record.quot_count=self.env['mrp.bom'].search_count(['name','=',record.name])

    @api.onchange('name')
    def set_upper(self):    
        if isinstance(self.name,str):
            force=self.env['ir.config_parameter'].get_param(PRODUCT_NAME_FORCE_UPPERCASE)
            self.name = str(self.name).upper() if force else str(self.name)
        return

    def _compute_bom_count(self):
        """ overrided method """
        for product in self:
            product.bom_count = self.env['mrp.bom'].search_count([('product_tmpl_id', '=', product.id),('type','!=','quot')])
            product.quot_count = self.env['mrp.bom'].search_count([('product_tmpl_id', '=', product.id),('type','=','quot')])

    
    def action_create_quotation(self):
        pass
    def action_view_quotations(self):
        pass