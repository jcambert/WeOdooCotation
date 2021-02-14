# -*- coding: utf-8 -*-

from odoo import models, fields, api

class WeIndice(models.Model):
    _inherit=['']
class WeProduct(models.Model):
    _inherit = ['product.template']
    cotations=fields.One2many('we.cotation','product')
    state=fields.Selection(selection_add=[('cotation', 'Cotation')],default='')