# -*- coding: utf-8 -*-
# from odoo.exceptions import AccessError, UserError
# from odoo import models, fields, api, _
# class WeWorkcenter(models.Model):
#     _inherit=['mrp.workcenter']

#     is_laser=fields.Boolean('Is Laser workcenter',default=False)
#     is_speed= fields.Boolean('Has different speed according material')

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
    

