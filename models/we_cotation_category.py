from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError,ValidationError
from ast import literal_eval as _literal_eval
from .models import Model
import logging
import re
import math
_logger = logging.getLogger(__name__)

class WeCotationPartnerPolitic(Model):
    _name='we.cotation.politic.partner'
    _description='Politic of cotation according partner'
    _inherit=['base.archive.mixin','base.sequence.mixin','mail.activity.mixin','mail.thread']

    name = fields.Char('Politic Name', required=True, translate=True)
    company_id = fields.Many2one('res.company', 'Company')
    partner_id = fields.Many2one(
        'res.partner', string='Customer', 
        required=True, change_default=True, index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    categories = fields.Many2many('we.cotation.category','we_cotation_category_rel','politic_id','category_id',string='Categories')

    def name_get(self):
        return [(politic.id, '%s (%s)' % (politic.name, politic.partner_id.name)) for politic in self]

class WeCotationCategory(Model):
    _name='we.cotation.category'
    _description='Category of Quotation eg Mo, Prep, Component, Sheetmetal, Sous-traitance for groupin price'
    _inherit=['base.archive.mixin']
    _sql_constraints = [
        ('we_cotation_category_name_uniq', 'unique (name)', "The name of category already exist!"),
    ]
    
    name=fields.Char('Name',required=True)
    category=fields.Many2one('product.category',required=True,string='Category')
    margin=fields.Float('Margin',default=0.0)
    

    @api.constrains('type','quotation_id')
    def _check_margin(self):
        if any(record.margin<0 for record in self ):
            raise UserError(_('Margin category must be greater or equal to zero'))
