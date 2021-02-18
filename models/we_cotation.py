# -*- coding: utf-8 -*-
from odoo.exceptions import AccessError, UserError
from odoo import models, fields, api, _
class WeCotation(models.Model):
    _name='we.cotation'
    _description='Quotation'
    # _inherit=['mail.activity.mixin','mail.thread']
    _sql_constraints = [
        ('we_cotation_cotation_name_uniq', 'unique (number,revision)', "The number/revision already exist!"),
    ]
    active = fields.Boolean(default=True)
    number = fields.Integer('Number',index=True, tracking=True,copy=False)
    revision = fields.Integer('Revision',index=True, tracking=True,copy=False)
    products = fields.Many2many('we.cotation.product')
    user_id=fields.Many2one('res.users','Responsable',ondelete='set null',help="responsable")
    create_date = fields.Datetime(string='Creation Date', readonly=True, index=True, help="Date on which cotation is created.")
    state=fields.Selection([('draft','Draft'), ('cotation', 'Cotation'),('closed','Closed')],default='draft')
    stage_id=fields.Many2one('we.cotation.stage',
        ondelete='restrict',
        help="Stage",
        compute='_compute_stage_id',
        group_expand='_read_group_stage_names',
        index=True, tracking=True,copy=False,readonly=False, store=True
        )
    workcenters=fields.One2many('we.cotation.workcenter','cotation')
    by_piece=fields.Boolean('By piece',default=True,tracking=True,help='If true then cotation piece by piece,for the affair otherwise')
    def _read_group_stage_names(self, stages, domain, order):
        search_domain=[]
        stages_ids = stages.search(search_domain)
        return stages_ids
    
    def _compute_stage_id(self):
        for record in self.filtered(lambda r: not r.stage_id):
            record.stage_id = record._stage_find(domain=[('fold', '=', False)]).id