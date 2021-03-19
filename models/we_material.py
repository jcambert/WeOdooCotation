# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError,ValidationError
from .models import Model

class WeMaterial(Model):
    _name='we.material'
    _description='Generic Material'
    _inherit=['base.sequence.mixin','base.archive.mixin','base.currency.mixin','mail.activity.mixin','mail.thread']
    _order='sequence'
    _sql_constraints = [
        ('material_name_uniq','unique(name)',"This name already exist !")
    ]
    sequence = fields.Integer('Sequence', default=1, help="Used to order material, First is default")
    name=fields.Char('Name',required=True,tracking=True)
    volmass=fields.Float('Volumic Mass',tracking=True, required=True,help="in m3/Kg")
    volmass_uom_id=fields.Many2one('uom.uom', string='Volumic mass measure', required=True)
    # purchase_ids=fields.One2many('we.purchase.material','material_id',string='Prices')
    unit_price=fields.Monetary('Unit price')
    price_uom_id=fields.Many2one('uom.uom', string='Price measure', required=True)

    @api.constrains
    def _check_unit_price(self):
        if any(record.unit_price<=0 for record in self):
            raise ValidationError(_('Unit price must be greater than 0'))

    @api.constrains('volmass')
    def _check_volmass(self):
        if any( record.volmass<=0 for record in self):
            raise ValidationError(_('The volumic mass must be greater than zero'))