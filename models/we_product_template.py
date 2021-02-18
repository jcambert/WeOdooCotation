# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WeProductTemplate(models.Model):
    """ Template Model for cotation processing
    """
    # _inherit = ['product.template']
    _name='we.cotation.product.template'
    _description='Cotation Product Templates'
    _order = "name"

    active = fields.Boolean(default=True,tracking=True)
    time_study = fields.Float('Study Duration', digits=(16, 2), default=9.0,help="Standard time study duration  (in minutes)",tracking=True)
    cost_study = fields.Integer('Study Cost',default='60',help="Standard cost study",tracking=True)
    cost_administrative = fields.Integer('Administrative Cost',default='45',help="Standard cost administative",tracking=True)
    cost_tool = fields.Integer('Tool Cost',default='0',help="Standard cost tool",tracking=True)
    material_margin = fields.Integer('Material Margin',default='35',help="Standard material margin (in percentage)",tracking=True)
    subcontracting_margin = fields.Integer('Subcontracting Margin',default='45',help="Standard subcontracting margin (in percentage)",tracking=True)
    note = fields.Char('Note',default='',tracking=True,help="Standard note")

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