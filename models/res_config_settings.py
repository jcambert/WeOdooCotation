from odoo import api, fields, models
import sys
from ast import literal_eval

SETTINGS='weSettings'
SHEETMETAL_CATEGORY='sheetmetal_category'
PRODUCT_NAME_FORCE_UPPERCASE='product_name_force_uppercase'
MATERIAL_ATTRIBUTE='material_attribute'
THICKNESS_ATTRIBUTE='thickness_attribute'
DIMENSION_ATTRIBUTE='dimension_attribute'
class WeSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    
    sheetmetal_category=fields.Many2one('product.category',default=False,config_parameter=SHEETMETAL_CATEGORY, string='Sheetmetal category')
    component_category=fields.Many2one('product.category',default=False,config_parameter='component_category',string='Product category')
    product_name_force_uppercase = fields.Boolean('Force name uppercase',default=False,config_parameter=PRODUCT_NAME_FORCE_UPPERCASE, help='Clear product material on name change')
    material_attribute = fields.Many2one('product.attribute',default=False,config_parameter=MATERIAL_ATTRIBUTE,string='Material attribute')
    thickness_attribute = fields.Many2one('product.attribute',default=False,config_parameter=THICKNESS_ATTRIBUTE,string='Thickness attribute')
    dimension_attribute = fields.Many2one('product.attribute',default=False,config_parameter=DIMENSION_ATTRIBUTE,string='Dimension attribute')