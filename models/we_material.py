# -*- coding: utf-8 -*-
from odoo.exceptions import AccessError, UserError
from odoo import models, fields, api, _
class WeGenericMaterialTemplate(models.Model):
    _name='we.cotation.generic.material.template'
    _inherit=['mail.activity.mixin','mail.thread']
    _description = 'Material Generic Description'
    _sql_constraints = [
        ('we_cotation_generic_material_name_uniq', 'unique (name)', "Name already exists !"),
    ]
    name=fields.Char('Name',required=True,tracking=True)
    volmass=fields.Float('Masse Volumic',digits=(16, 2), required=True)
    materials=fields.One2many('we.cotation.material.template','material')
    @api.constrains('volmass')
    def _on_volmass(self):
        if any( record.volmass<0 for record in self):
            raise UserError(_('Volumic mass must be greater than zero'))

class WeMaterialTemplate(models.Model):
    _name='we.cotation.material.template'
    _description='Material Description'
    _sql_constraints = [
        ('we_cotation_material_name_uniq', 'unique (name)', "Name already exists !"),
    ]
    name=fields.Char('Name',required=True)
    material=fields.Many2one('we.cotation.generic.material.template','materials')

class WeMaterial(models.Model):
    _name='we.cotation.material'
    _description='Material used in operation'
    cotation = fields.Many2one('we.cotation','matieres')