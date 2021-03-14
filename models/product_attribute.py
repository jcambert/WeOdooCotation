# -*- coding: utf-8 -*-
from odoo import fields
from .models import Model


class ProductAttribute(Model):
    _inherit = 'product.attribute'
    display_type = fields.Selection( selection_add=[
        ('dimension','Dimension'),
        ('thickness','Thickness'),
        ('material','Material')], 
        ondelete={'dimension': 'cascade','thickness': 'cascade','material': 'cascade',})

class ProductAttributeValue(Model):
    _inherit = 'product.attribute.value'
    """ 3 Dimensionnal abilities """
    length = fields.Float('Length',default=0.0)
    width = fields.Float('Width',default=0.0)
    thickness = fields.Float('Thickness',default=0.0)
    material = fields.Many2one('we.material','Material')
    volmass = fields.Float('Volumic mass',related='material.volmass')