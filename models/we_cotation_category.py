from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError,ValidationError
from ast import literal_eval as _literal_eval
from .models import Model
import logging
import re
import math
_logger = logging.getLogger(__name__)

class WeCotationCategory(models.Model):
    _name='we.cotation.category'
    _description='Category of Quotation eg Mo, Prep, Component, Sheetmetal, Sous-traitance for groupin price'
    _sql_constraints = [
        ('we_cotation_category_name_uniq', 'unique (name)', "The name of category already exist!"),
    ]
    active=fields.Boolean('Active',default=True)
    name=fields.Char('Name',required=True)
    category=fields.Many2one('product.category',required=True,string='Category')
    margin=fields.Float('Margin',default=0.0)

    @api.constrains('type','quotation_id')
    def _check_margin(self):
        if any(record.margin<0 for record in self ):
            raise UserError(_('Margin category must be greater or equal to zero'))
