# -*- coding: utf-8 -*-
from odoo.exceptions import AccessError, UserError
from odoo import models, fields, api, _
class WeCotationBom(models.Model):
    """ Defines bills of material for a product in Quotation  """
    _name='we.cotation.bom'
    _description = 'Bill of Material Quotation'
    _inherit = ['mail.thread']
    _rec_name = 'product'
    _order='sequence'
    _check_company_auto = True

    def _get_default_product_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id').id
        
    active = fields.Boolean('Active', default=True,help="If the active field is set to False, it will allow you to hide the bills of material without removing it.")
    product = fields.Many2one('we.cotation.product', 'Product',check_company=True,domain="[ '|', ('company_id', '=', False), ('company_id', '=', company_id)]", required=True)
    bom_lines = fields.One2many('we.cotation.bom.line', 'bom', 'BoM Lines', copy=True)
    product_qty = fields.Float('Quantity', default=1.0,digits='Unit of Measure', required=True)
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure',default=_get_default_product_uom_id, required=True,help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control", domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product.uom_id.category_id')
    
    sequence = fields.Integer('Sequence', help="Gives the sequence order when displaying a list of bills of material.")
    # operations = fields.One2many('mrp.routing.workcenter', 'bom_id', 'Operations', copy=True)   
    company_id = fields.Many2one('res.company', 'Company', index=True,default=lambda self: self.env.company)


class WeCotationBomLine(models.Model):
    _name = 'we.cotation.bom.line'
    _order = "sequence, id"
    _rec_name = "product"
    _description = 'Bill of Material Line'
    _check_company_auto = True

    product = fields.Many2one('we.cotation.product', 'Component', required=True, check_company=True)
    product_qty = fields.Float('Quantity', default=1.0,digits='Product Unit of Measure', required=True)
    product_uom = fields.Many2one('uom.uom', 'Product Unit of Measure',default='_get_default_product_uom_id',required=True,help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control", domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product.uom_id.category_id')
    sequence = fields.Integer('Sequence', default=1,help="Gives the sequence order when displaying.")
    bom = fields.Many2one('we.cotation.bom', 'Parent BoM', index=True, ondelete='cascade', required=True)
    company_id = fields.Many2one(related='bom.company_id', store=True, index=True, readonly=True)
    
    def _get_default_product_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id').id
    