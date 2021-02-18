# -*- coding: utf-8 -*-
from odoo.exceptions import AccessError, UserError
from odoo import models, fields, api, _
class WeCotationBom(models.Model):
    _name='we.cotation.bom'