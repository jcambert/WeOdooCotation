# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError,ValidationError


class WeProductTemplate(models.Model):
    """ Template Model for cotation processing
    """
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name='we.cotation.product.template'
    _description='Cotation Product Templates'
    _order = "name"
    name = fields.Char('Template Name', required=True, tracking=True,default=_("Default"))
    active = fields.Boolean(default=True,tracking=True)
    time_study = fields.Float('Study Duration', digits=(16, 2), default=9.0,help="Standard time study duration  (in minutes)")
    cost_study = fields.Integer('Study Cost',default='60',help="Standard cost study")
    cost_administrative = fields.Integer('Administrative Cost',default='45',help="Standard cost administative")
    cost_tool = fields.Integer('Tool Cost',default='0',help="Standard cost tool")
    material_margin = fields.Integer('Material Margin',default='35',help="Standard material margin (in percentage)")
    subcontracting_margin = fields.Integer('Subcontracting Margin',default='45',help="Standard subcontracting margin (in percentage)")
    note = fields.Char('Note',default='',help="Standard note")

    @api.constrains('time_study')
    def _check_time_study(self):
        if any( record.time_study<0 for record in self):
            raise ValidationError(_('Time study must be greater than 0'))
    @api.constrains('cost_study')
    def _check_cost_study(self):
        if any( record.cost_study<0 for record in self):
            raise ValidationError(_('Cost study must be greater than 0'))
    @api.constrains('cost_administrative')
    def _check_cost_administrative(self):
        if any( record.cost_administrative<0 for record in self):
            raise ValidationError(_('Cost administrative must be greater than 0'))
    @api.constrains('cost_tool')
    def _check_cost_tool(self):
        if any( record.cost_tool<0 for record in self):
            raise ValidationError(_('Cost tool must be greater than 0'))
    @api.constrains('material_margin')
    def _check_material_margin(self):
        if any( record.material_margin<0 for record in self):
            raise ValidationError(_('Material margin must be greater than 0'))
    @api.constrains('subcontracting_margin')
    def _check_subcontracting_margin(self):
        if any( record.subcontracting_margin<0 for record in self):
            raise ValidationError(_('Subcontracting margin must be greater than 0'))