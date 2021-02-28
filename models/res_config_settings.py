from odoo import api, fields, models
import sys
from ast import literal_eval

SETTINGS='weSettings'
PRODUCT_NAME_FORCE_UPPERCASE='product_name_force_uppercase'
class WeSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    
    sheetmetal_category=fields.Many2one('product.category',default=False,config_parameter='sheetmetal_category', string='Sheetmetal category')
    # profile_categories=fields.Many2many('product.category',string='Profiles categories')
    component_category=fields.Many2one('product.category',default=False,config_parameter='component_category',string='Product category')
    # material_convention_names=fields.Many2many('we.setting.tag', 'we_setting_material_tag_rel', 'setting_id', 'material_tag_id', string='Material convention name')
    # sheetmetal_convention_names=fields.Many2many('we.setting.tag', 'we_setting_sheetmetal_tag_rel', 'setting_id', 'sheetmetal_tag_id', string='Sheetmetal convention name')
    # profile_convention_names=fields.Many2many('we.setting.tag', 'we_setting_profile_tag_rel', 'setting_id', 'profile_tag_id', string='Profile convention name')
    
    # clear_product_on_category_change = fields.Boolean('Clear on category change', help='Clear product material on category change',default=False)
    # clear_product_on_name_change = fields.Boolean('Clear on name Change', help='Clear product material on name change',default=False)
    product_name_force_uppercase = fields.Boolean('Force name uppercase',default=False,config_parameter='product_name_force_uppercase', help='Clear product material on name change')
  
    # indice_for_purchased = fields.Boolean('Indice for purchased product', help='Indice for purchased product',default=False)

    # def get_param(self,key):
    #     return super(WeSettings,'%s.%s' % (SETTINGS,key))
    # def _set_values(self,fn,key,value):
    #     fn('%s.%s' % (SETTINGS,key),value)
    # def _get_values(self,fn,key):
    #     return fn('%s%s'%(SETTINGS, key))
    # def set_values(self):
    #     res=super(WeSettings, self).set_values()
    #     fn=self.env['ir.config_parameter'].set_param
    #     self._set_values(fn,'sheetmetal_category',self.sheetmetal_category.id or False)
    #     self._set_values(fn,'component_category',self.component_category.id or False)
        # self._set_values(fn,'profile_categories',self.profile_categories.ids or [])
        # self._set_values(fn,'material_convention_names',self.material_convention_names.ids or [])
        # self._set_values(fn,'sheetmetal_convention_names',self.sheetmetal_convention_names.ids or [])
        # self._set_values(fn,'profile_convention_names',self.profile_convention_names.ids or [])

        # self._set_values(fn,'clear_product_on_category_change',self.clear_product_on_category_change)
        # self._set_values(fn,'clear_product_on_name_change',self.clear_product_on_name_change)
        # self._set_values(fn,'indice_for_purchased',self.indice_for_purchased)
        # fn('product_name_force_uppercase',self.product_name_force_uppercase or False)


        # return res
    
    # @api.model
    # def get_values(self):
    #     res = super(WeSettings, self).get_values()
    #     try:
    #         fn = self.env['ir.config_parameter'].sudo().get_param
    #         sheetmetal_category=self._get_values(fn,'sheetmetal_category') or False
    #         component_category=self._get_values(fn,'component_category') or False
            # profile_categories=self._get_values(fn,'profile_categories') or False
            # material_convention_names=self._get_values(fn,'material_convention_names') or False
            # sheetmetal_convention_names=self._get_values( fn,'sheetmetal_convention_names') or False
            # profile_convention_names=self._get_values(fn,'profile_convention_names') or False

            # clear_product_on_category_change=self._get_values(fn,'clear_product_on_category_change') or False
            # clear_product_on_name_change=self._get_values(fn,'clear_product_on_name_change') or False
            # product_name_force_uppercase=self._get_values(fn,PRODUCT_NAME_FORCE_UPPERCASE) or False
            # indice_for_purchased=self._get_values(fn,'indice_for_purchased') or False

            

            # updates={}
            # if isinstance(sheetmetal_category,str) :
            #     updates['sheetmetal_category']=literal_eval(sheetmetal_category)
            # if isinstance(component_category,str) :
            #     updates['component_category']=literal_eval(component_category)
            # if isinstance(profile_categories,str):
            #     updates['profile_categories']=literal_eval(profile_categories)
            # if isinstance(material_convention_names,str):
            #     updates['material_convention_names']=literal_eval(material_convention_names)
            # if isinstance(sheetmetal_convention_names,str):
            #     updates['sheetmetal_convention_names']=literal_eval(sheetmetal_convention_names)
            # if isinstance(profile_convention_names,str):
            #     updates['profile_convention_names']=literal_eval(profile_convention_names)
            
            # updates['clear_product_on_category_change']=clear_product_on_category_change
            # updates['clear_product_on_name_change']=clear_product_on_name_change
            # updates['product_name_force_uppercase']=product_name_force_uppercase
            # updates['indice_for_purchased']=indice_for_purchased

        #     res.update(updates)
        # except :
        #     print("Unexpected error:", sys.exc_info()[0])
        #     raise
        # return res