# -*- coding: utf-8 -*-
from odoo.exceptions import AccessError, UserError
from odoo import models, fields, api, _

class WeWorkcenterTemplate(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name ='we.cotation.workcenter.template'
    _description='Operation available for all new cotation'
    name=fields.Char('Name',required=True,tracking=True)
    active = fields.Boolean('Active',tracking=True, default=True, store=True, readonly=False)
    helps = fields.Char('Operation Help',default='')
    cost_time_prep_pr=fields.Integer('Cost Time PR Preparation',default='0',tracking=True,help="Cost time pr for preparation")
    cost_time_exec_pr=fields.Integer('Cost Time PR Execution',default='0',tracking=True,help="Cost time pr for execution")
    cost_time_prep_pv=fields.Integer('Cost Time PV Preparation',default='0',tracking=True,help="Cost time pv for preparation")
    cost_time_exec_pv=fields.Integer('Cost Time PV Execution',default='0',tracking=True,help="Cost time pv for execution")
    default_time_prep=fields.Float('Default Time for preparation',digits=(2, 1),tracking=True,required=True)
    base_time=fields.Float('Base time execution',digits=(16, 5) ,tracking=True,required=True)

    cotation=fields.One2many('we.cotation','workcenters')

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

class WeWorkcenter(models.Model):
    """
        Copy of Operation Template into cotation
        that permit to make changes into this cotation, without changing all
    """
    _inherit=['we.cotation.workcenter.template']
    _name='we.cotation.workcenter'
    _description='Operation available for a cotation'
    operations = fields.Many2one('we.cotation.operation',string='Operation')
    cotation = fields.Many2one('we.cotation',string='Quotation')
    
class WeOperation(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name='we.cotation.operation'
    _description='Operation for a product cotation'
    _order = "sequence, name, id"
    
    name = fields.Char('Operation Name', required=True, tracking=True)
    
    sequence = fields.Integer('Sequence', default=1, help="Used to order operations.")
    workcenter = fields.One2many('we.cotation.workcenter',inverse_name='operations',string='Workcenter',required=True)
    #this can be a char, thus it can bena formula
    qty = fields.Char('Quantity',required=True,tracking=True)
    qty_value = fields.Float('Quantity value',compute='_compute_quantity')
    fold=fields.Boolean(string="Replié en vue kanban")

    @api.depends('qty')
    def _compute_quantity(self):
        for record in self:
            try:
                code=compile(record.qty, "<string>", "eval")
                record.qty_value=float(eval(code))
            except:
                
                raise UserError(_('This is not a valid quantity'))
