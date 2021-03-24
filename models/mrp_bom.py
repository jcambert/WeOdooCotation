from odoo.exceptions import AccessError, UserError
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

class WeBomLine(Model):
    _inherit = 'mrp.bom.line'

    def get_calcul_domain(self):
        return [('category_id.id', '=', self.get_param(UOM_VOLUMIC_MASS))]
    calcul_id=fields.Many2one('we.cotation.bom.line.calculation',string='Calcul',domain=lambda r:r.get_calcul_domain())

    
