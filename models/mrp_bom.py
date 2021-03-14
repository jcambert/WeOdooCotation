from odoo.exceptions import AccessError, UserError
from odoo import models, fields, api, _
from .models import Model

class WeBom(Model):
    _inherit='mrp.bom'

    type = fields.Selection(selection_add=[('quot','Quotation')], ondelete={'quot': 'cascade'})
    quotation_line_ids = fields.One2many('we.cotation.order.line','product_bom',string='Quotation Lines')
    

class WeBomLine(Model):
    _inherit = 'mrp.bom.line'

    
