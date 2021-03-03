# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'
    display_type = fields.Selection( selection_add=[('dimension','Dimension')], ondelete={'dimension': 'cascade'})

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    length = fields.Float('Length',default=0.0)
    width = fields.Float('Width',default=0.0)