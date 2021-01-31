# -*- coding: utf-8 -*-
from odoo.exceptions import AccessError, UserError
from odoo import models, fields, api, _
class WeCotation(models.Model):
    _name='we.cotation'
    _inherit=['mail.activity.mixin','mail.thread']
    _sql_constraints = [
        ('name_uniq', 'unique (number,revision)', "The number/revision already exist!"),
    ]
    active = fields.Boolean(default=True)
    number = fields.Integer('Number',index=True, tracking=True,copy=False,)
    revision = fields.Integer('Revision',index=True, tracking=True,copy=False,)
    product = fields.Many2one('product.template', 'Product',auto_join=True, ondelete="set null")
    user_id=fields.Many2one('res.users','Responsable',ondelete='set null',help="responsable")
    create_date = fields.Datetime(string='Creation Date', readonly=True, index=True, help="Date on which cotation is created.")

