# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError,ValidationError
from ast import literal_eval
import logging
import re
import math

class BeamType(models.Model):
    _name='we.beam.type'
    _description='Standard Profile Type' #UPN HEA ..
    _inherit=['we.convention']
    _order='name'
    _sql_constraints = [
        ('name_uniq','unique(name)',"The name of this profile type must be unique"),
    ]
    name=fields.Char('Type',required=True)
    length=fields.Float('Length',default=0.0)
    width=fields.Float('Width',default=0.0)
    default_length=fields.Integer('Default length',default=0.0)
    # convention=fields.Char('Convention',required=True,help="python regex string convention")
    calculate_surface_section=fields.Char('Surface section formula',default='')
    calculate_surface_meter=fields.Char('Surface meter formula',default='')
    calculate_dim2=fields.Char('Dimension 2 formula',default='')
    calculate_dim3=fields.Char('Dimension 3 formula',default='')
    calculate_dim4=fields.Char('Dimension 4 formula',default='')

    @api.onchange('calculate_surface_section')
    def _on_change_calculate_surface_section(self):
        for record in self.filtered(lambda r:isinstance(r.calculate_surface_section,str)):
            record.calculate_surface_section=record.calculate_surface_section.strip()
    @api.onchange('calculate_surface_meter')
    def _on_change_calculate_surface_meter(self):
        for record in self.filtered(lambda r:isinstance(r.calculate_surface_meter,str)):
            record.calculate_surface_meter=record.calculate_surface_meter.strip()
    @api.onchange('calculate_dim2')
    def _on_change_calculate_dim2(self):
        for record in self.filtered(lambda r:isinstance(r.calculate_dim2,str)):
            record.calculate_dim2=record.calculate_dim2.strip()
    @api.onchange('calculate_dim3')
    def _on_change_calculate_dim3(self):
        for record in self.filtered(lambda r:isinstance(r.calculate_dim3,str)):
            record.calculate_dim3=record.calculate_dim3.strip()
    @api.onchange('calculate_dim4')
    def _on_change_calculate_dim4(self):
        for record in self.filtered(lambda r:isinstance(r.calculate_dim4,str)):
            record.calculate_dim4=record.calculate_dim4.strip()
    


class Beam(models.Model):
    _name='we.beam'
    _description='Standard Beam Dimension'
    _sql_constraints = [
        ('we_beam_name_uniq','unique(type_id,name)',"The name of this beam type must be unique"),
    ]
    name=fields.Char('Name',required=True,index=True)
    type_id=fields.Many2one('we.beam.type','Type',required=True)
    surface_section=fields.Float('Surface',default=0.0)
    surface_meter=fields.Float('Surface meter',default=0.0)
    weight_meter=fields.Float('Weight meter',default=0.0)