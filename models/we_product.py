# -*- coding: utf-8 -*-

from odoo import models, fields, api
class WeProduct(models.Model):
    _inherit = ['product.template']
    cotations=fields.One2many('we.cotation','product')