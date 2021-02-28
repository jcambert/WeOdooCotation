from odoo.exceptions import AccessError, UserError
from odoo import models, fields, api, _

class WeWorkcenter(models.Model):
    _inherit=['mrp.workcenter']

    
    is_speed= fields.Boolean('Has different speed according material',compute='_compute_is_speed')

    quot_cost = fields.Float(string='Execution', help='Specify quotation cost of work center per hour.', default=0.0)
    quot_help = fields.Char('Operation information',default='')
    quot_cost_prep=fields.Integer('Preparation',help="Cost time pr for preparation",default=0)
    # quot_cost_time_exec=fields.Integer('Cost Time PR Execution',help="Cost time pr for execution",default=0)
    quot_default_time_prep=fields.Float('Default Time for preparation',digits=(2, 1),required=True,default=0.0)
    quot_base_time=fields.Float('Base time execution',digits=(16, 5) ,required=True,default=0.0)
    quot_margin=fields.Float(string='Margin',store=True,help='Margin belongs to cost Hour',readonly=True,compute='_compute_quotation_margin')
    
    time_cycle_prep = fields.Float('Preparation Duration',default=0.0)

    @api.constrains('quot_cost')
    def _check_quot_cost(self):
        if any( record.quot_cost<0 for record in self):
            raise UserError(_('Quotation execution cost time must be greater or equal to zero'))
    @api.constrains('quot_cost_time_prep')
    def _check_quot_cost_time_prep(self):
        if any( record.quot_cost_time_prep<0 for record in self):
            raise UserError(_('Quotation preparation cost time must be greater or equal to zero'))
    @api.constrains('quot_default_time_prep')
    def _check_quot_default_time_prep(self):
        if any( record.quot_default_time_prep<0 for record in self):
            raise UserError(_('Quotation default time preparation must be greater or equal to zero'))
    @api.constrains('quot_base_time')
    def _check_quot_base_time(self):
        if any( record.quot_base_time<0 for record in self):
            raise UserError(_('Quotation base time must be greater or equal to zero'))
    # @api.onchange('costs_hour')
    # def _on_costs_hour_change(self):


    def _compute_is_speed(self):
        return False

    @api.depends('costs_hour','quot_cost')
    def _compute_quotation_margin(self):
        for workcenter in self:
            workcenter.quot_margin=workcenter.costs_hour / workcenter.quot_cost if workcenter.quot_cost>0 else 0.0

class WeWorkcenterSpeed(models.Model):
    _name='mrp.workcenter.speed'
    _description='Workkcenter speed according material/thickness, ...'

# class WeWorkcenterSpeedTemplate(models.Model):
#     _name='we.cotation.workcenterspeed.template'
#     _sql_constraints = [
#         ('name_uniq', 'unique (name)', "Name already exists !"),
#     ]
#     name=fields.Char('Name',required=True)
#     workcenter=fields.Many2one('mrp.worcenter')


# class WeWorkcenterSpeed(models.Model):
#     _name='we.cotation.workcenterspeed'
#     workcenter=fields.Many2one('mrp.worcenter')
#     material=fields.One2many('we.generic.material')
#     thickness=fields.Float('Thickness')
#     speed=fields.Integer('Speed')
    

