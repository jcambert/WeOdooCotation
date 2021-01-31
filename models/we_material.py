# -*- coding: utf-8 -*-
from odoo.exceptions import AccessError, UserError
from odoo import models, fields, api, _
class WeGenericMaterial(models.Model):
    _name='we.generic.material'
    _description = 'Material Generic Description'
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Name already exists !"),
    ]
    name=fields.Char('Name',required=True)
    masse_v=fields.Float('Masse Volumic',required=True)
    materials=fields.One2many('we.material','material')
    @api.onchange('masse_v')
    def _on_massev_changed(self):
        for record in self:
            if record.masse_v<=0:
                raise UserError(_('Volumic mass must be greater than zero'))

class WeMaterial(models.Model):
    _name='we.material'
    _description='Material Description'
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Name already exists !"),
    ]
    name=fields.Char('Name',required=True)
    material=fields.Many2one('we.generic.material','Material')