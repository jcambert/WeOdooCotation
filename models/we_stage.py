# -*- coding: utf-8 -*-
from odoo.exceptions import AccessError, UserError
from odoo import models, fields, api, _
class WeCotationStage(models.Model):
    """ Model for case stages. This models the main stages of a document
        management flow. Main Cotation objects (leads, opportunities, project
        issues, ...) will now use only stages, instead of state and stages.
        Stages are for example used to display the kanban view of records.
    """
    _name='we.cotation.stage'
    _description='Cotation Stages'
    _order = "sequence, name, id"
    
    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    fold=fields.Boolean(string="Replié en vue kanban")
