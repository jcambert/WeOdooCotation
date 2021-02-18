# -*- coding: utf-8 -*-
from odoo.exceptions import AccessError, UserError
from odoo import models, fields, api, _

class WeWorkcenterTemplate(models.Model):
    _name ='we.cotation.workcenter.template'
    _description='Operation available for all new cotation'
    name=fields.Char('Operation Name',required=True,tracking=True)
    active = fields.Boolean('Active',tracking=True, default=True, store=True, readonly=False)
    helps = fields.Char('Operation Help',default='')
    cost_time_prep_pr=fields.Integer('Cost Time PR Preparation',default='0',help="Cost time pr for preparation",tracking=True)
    cost_time_exec_pr=fields.Integer('Cost Time PR Execution',default='0',help="Cost time pr for execution",tracking=True)
    cost_time_prep_pv=fields.Integer('Cost Time PV Preparation',default='0',help="Cost time pv for preparation",tracking=True)
    cost_time_exec_pv=fields.Integer('Cost Time PV Execution',default='0',help="Cost time pv for execution",tracking=True)
    default_time_prep=fields.Float('Default Time for preparation',digits=(2, 1),required=True,tracking=True)
    base_time=fields.Float('Base time execution',digits=(16, 5) ,required=True,tracking=True)

    cotation=fields.Many2one('we.cotation','workcenters')

    @api.constrains('cost_time_prep_pr')
    def _check_cost_time_prep_pr(self):
        if any( record.cost_time_prep_pr<0 for record in self):
            raise UserError(_('Cost Time PR Preparation must be greater than zero'))
    @api.constrains('cost_time_exec_pr')
    def _check_cost_time_exec_pr(self):
        if any( record.cost_time_exec_pr<0 for record in self):
            raise UserError(_('Cost Time PR Execution must be greater than zero'))
    @api.constrains('cost_time_prep_pv')
    def _check_cost_time_prep_pv(self):
        if any( record.cost_time_prep_pv<0 for record in self):
            raise UserError(_('Cost Time PV Preparation must be greater than zero'))
    @api.constrains('cost_time_exec_pv')
    def _check_cost_time_exec_pv(self):
        if any( record.cost_time_exec_pv<0 for record in self):
            raise UserError(_('Cost Time PV Execution must be greater than zero'))
    @api.constrains('default_time_prep')
    def _check_default_time_prep(self):
        if any( record.default_time_prep<0 for record in self):
            raise UserError(_('Default Time for preparation must be greater than zero'))
    @api.constrains('base_time')
    def _check_base_time(self):
        if any( record.base_time<0 for record in self):
            raise UserError(_('Base time execution must be greater than zero'))

class WeWorkcenter(WeWorkcenterTemplate):
    """
        Copy of Operation Template into cotation
        that permit to make changes into this cotation, without changing all
    """
    _name='we.cotation.workcenter'
    _description='Operation available for a cotation'
    

class WeOperation(models.Model):
    _name='we.cotation.operation'
    _description='Operation for a product cotation'
    _order = "sequence, name, id"
    
    name = fields.Char('Operation Name', required=True, tracking=True)
    
    sequence = fields.Integer('Sequence', default=1, help="Used to order operations.")
    fold=fields.Boolean(string="Replié en vue kanban")
