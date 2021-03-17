# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError,ValidationError
from .models import Model

class WeMaterial(Model):
    _name='we.material'
    _description='Generic Material'
    # _inherit=['sequence.mixin']
    _order='sequence'
    _sql_constraints = [
        ('material_name_uniq','unique(name)',"This name already exist !")
    ]
    sequence = fields.Integer('Sequence', default=1, help="Used to order material, First is default")
    name=fields.Char('Name',required=True)
    volmass=fields.Float('Volumic Mass',required=True,help="in m3/Kg")
    

    @api.constrains('volmass')
    def _check_volmass(self):
        if any( record.volmass<=0 for record in self):
            raise ValidationError(_('The volumic mass must be greater than zero'))