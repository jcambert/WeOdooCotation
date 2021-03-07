from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError,ValidationError
from ast import literal_eval as _literal_eval
from .models import Model
import logging
import re
import math
_logger = logging.getLogger(__name__)
from .res_config_settings import PRODUCT_NAME_FORCE_UPPERCASE,DIMENSION_ATTRIBUTE,THICKNESS_ATTRIBUTE,MATERIAL_ATTRIBUTE,SHEETMETAL_CATEGORY
def literal_eval(arg):
    if isinstance(arg,bool):
        return arg
    return _literal_eval(arg)
def _filterByRe(*args):
    if len(args) not in [2,3]:
        return False
    convention,name,res=args[0],args[1],args[2] if len(args)==3 else None
    if(not convention or not name or len(convention)==0 or len(name)==0):
        return False
    _logger.info(f"Filtering: Convention->{convention} , name->{name}")
    p = re.compile(convention,re.IGNORECASE)
    m = p.match(name)
    if m:
        if isinstance(res,dict):
            res.update(m.groupdict())
        return True
    return False

def _compile(code,backfn,errorfn):
    if not isinstance(code,str):
        return
    try:
        _code = compile(code, "<string>", "eval")
        backfn(eval(code))
    except:
        errorfn()

class ProductTemplate(Model):
    _inherit = ['product.template']
    _description = 'Product Quotation Extensions'

    libelle = fields.Char('Libelle')
    quot_count = fields.Integer('Quotation',compute='_compute_bom_count', compute_sudo=False)
    material = fields.Many2one('we.material','Material')
    is_sheetmetal=fields.Boolean()
    is_beam=fields.Boolean()
    is_predefined_beam=fields.Boolean('Is predefined beam')
    def _compute_quotation_count(self):
        for record in self:
            record.quot_count=self.env['mrp.bom'].search_count(['name','=',record.name])

    @api.onchange('name')
    def set_upper(self):    
        if isinstance(self.name,str):
            force=self.get_param(PRODUCT_NAME_FORCE_UPPERCASE)
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

class Product(Model):
    _inherit = "product.product"
    _models={'attribute':'product.attribute','material':'we.material'}
    
    beam_length = fields.Integer('Beam length')
    surface_section = fields.Float('Surface Section', digits='Product Unit of Measure', default=0.0)
    surface_meter = fields.Float('Surface per meter', digits='Product Unit of Measure', default=0.0)
    weight_meter = fields.Float('Weight per meter', digits='Product Unit of Measure', default=0.0)
    dim1=fields.Float('dim1',digits='Product Unit of Measure',default=0.0)#length, external diameter
    dim2=fields.Float('dim2',digits='Product Unit of Measure',default=0.0)#Width, external diameter
    dim3=fields.Float('dim3',digits='Product Unit of Measure',default=0.0)#Length, internal diameter
    dim4=fields.Float('dim4',digits='Product Unit of Measure',default=0.0)#Width, internal diameter
    dim5=fields.Float('dim5',digits='Product Unit of Measure',default=0.0)#thickness

    volmass=fields.Float('Volumic mass',default=0.0,related='material.volmass')
    auto_surface=fields.Float('Auto calculated surface',store=True,compute='_compute_material_values', digits='Product Unit of Measure',default=0.0)
    auto_weight=fields.Float('Auto calculated weight',store=True,compute='_compute_material_values',default=0.0)

    @api.onchange('name')
    def set_upper(self):    
        if isinstance(self.name,str):
            force=self.get_param(PRODUCT_NAME_FORCE_UPPERCASE)
            self.name = str(self.name).upper() if force else str(self.name)
        return
    
    @api.depends('product_template_attribute_value_ids')
    def _compute_material_values(self):
        dim_id= self.get_param(DIMENSION_ATTRIBUTE)
        thickness_id= self.get_param(THICKNESS_ATTRIBUTE)
        material_id=self.get_param(MATERIAL_ATTRIBUTE)
        sheetmetal_id = self.get_param(SHEETMETAL_CATEGORY)
        # dim_attr=  self.env['product.attribute'].browse(dim_id) 
        dim_attr=self.attribute.browse(dim_id)
        thickness_attr=  self.env['product.attribute'].browse(thickness_id) 
        material_attr=self.env['product.attribute'].browse(material_id) 
        for record in self:
            record.is_sheetmetal =self.categ_id.id ==  sheetmetal_id
            if dim_attr:
                _dim_attr = record.product_template_attribute_value_ids.filtered(lambda r:r.attribute_id.id==dim_attr.id)
                if _dim_attr:
                    record.dim1=_dim_attr.product_attribute_value_id.length
                    record.dim2=_dim_attr.product_attribute_value_id.width
            if thickness_attr:
                _thickness_attr = record.product_template_attribute_value_ids.filtered(lambda r:r.attribute_id.id==thickness_attr.id)
                if _thickness_attr:
                    record.dim5=_thickness_attr.product_attribute_value_id.thickness
            if material_attr:
                _material_attr = record.product_template_attribute_value_ids.filtered(lambda r:r.attribute_id.id==material_attr.id)
                if _material_attr:
                #     material=self.material.search([('name','=',_material_attr.product_attribute_value_id.name)],limit=1)
                #     if material:
                #         record.material=material
                #     else:
                    record.material=_material_attr.product_attribute_value_id.material.id

            record.auto_surface=0.0
            record.auto_weight=0.0
            record.calculate_weight()
            # record.weight=(record.dim1*record.dim2*record.dim5*volmass)/1000000

    @api.model
    def calculate_weight(self):
        self.ensure_one()
        self.weight=(self.dim1*self.dim2*self.dim5*self.volmass)/1000000
    
    @api.onchange('dim1','dim2','dim5','volmass')
    def _on_dim1_change(self):
        for record in self:
            record.calculate_weight()
    @api.model
    def compute_is_beam(self,beams,beam_ids,sheetmetal_id,beam_types,materials,clear_cat=False,clear_name=False):
        self.ensure_one()
        if not self.categ_id.id:
            self.is_beam=False
            return
        self.is_beam = self.categ_id.id in literal_eval(beam_ids) if isinstance(beam_ids,str)  else profile_ids
        self.is_sheetmetal = self.categ_id.id ==  literal_eval( sheetmetal_id) if isinstance(sheetmetal_id,str)  else sheetmetal_id
        if True not in (self.is_beam ,self.is_sheetmetal):
            return
        groups={}
        beam=beams.filtered(lambda r:_filterByRe(r.type_id.convention,self.name,groups))
        if beam.exists() and beam.ensure_one():
            self.is_predefined_beam=True
            self.beam_type=beam
            try:
                p = re.compile(beam.type_id.convention)
                m = p.match(self.name)
                value=m.groupdict()['value']
                # print('value: %s' %(value))
                candidate=beam.filtered(lambda r:r.name==value)
                if candidate.exists():
                    self.profile_length=self.profile_length if self.profile_length>0 else beam.type_id.default_length
                    self.surface_section= self.surface_section if self.surface_section>0 else candidate[0].surface_section
                    self.surface_meter= self.surface_meter if self.surface_meter>0 else candidate[0].surface_meter 
                    self.weight_meter=self.weight_meter if self.weight_meter>0 else candidate[0].weight_meter
                    # record.material set to first finded
                if 'material' in groups:
                    material=materials.filtered(lambda r:_filterByRe(r.convention,groups['material']))
                    if material.exists() :
                        self.material=material[0]
                else:
                    material=materials.filtered(lambda r:r.default)
                    if material.exists() :
                        self.material=material[0]

                if 'thickness' in groups:
                    self.dim5=float(groups['thickness'])
            except:
                raise
        else:
            self.is_predefined_beam=False
            groups={}
            beam=beam_types.filtered(lambda r:self._filterByRe(r.convention,self.name,groups))
            if profile.exists() and beam.ensure_one():
                self.beam_type=beam
                if clear_name or clear_cat:
                    self.beam_length=0
                    self.dim1=self.dim2=self.dim3=self.dim4=self.dim5=0.0
                thickness=0.0
                value=value_one=value_two=0
                self.beam_length= self.beam_length if self.beam_length>0 else int(beam.default_length)
                if self.is_sheetmetal:
                    value=value_one=self.dim1= self.dim1 if self.dim1>0 else beam.length
                    value_two=self.dim2= self.dim2 if self.dim2>0 else beam.width
                elif 'value' in groups:
                    value=self.dim1=int(groups['value'])
                if 'value_one' in groups:
                    value_one=self.dim1=int(groups['value_one'])
                if 'value_two' in groups:
                    value_two=self.dim2=int(groups['value_two'])
                if 'thickness' in groups:
                    thickness=self.dim5=self.dim5 if self.dim5>0 else float(groups['thickness'])
                    # self.dim2=self.dim1-2*self.dim5
                if 'material' in groups:
                    material=materials.filtered(lambda r:_filterByRe(r.convention,groups['material']))
                    if material.exists() :
                        self.material=material[0]
                else:
                    material=materials.filtered(lambda r:r.default)
                    if material.exists()  :
                        self.material=material[0]
                if 'finition' in groups:
                    self.finition=groups['finition']
                self._update_non_standard_profile_values()