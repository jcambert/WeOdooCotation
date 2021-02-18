# -*- coding: utf-8 -*-

from odoo import models, fields, api
class WeProduct(models.Model):
    """ Model for cotation processing
    """
    # _inherit = ['product.template']
    _name='we.cotation.product'
    _description='Cotation Products'
    _order = "name"
    _sql_constraints = [
        ('we_cotation_product_name_uniq', 'unique (name,revision)', "The number/revision already exist!"),
    ]
    active = fields.Boolean(default=True,tracking=True)
    cotations=fields.Many2many('we.cotation')
    name = fields.Char('Product Name', required=True, tracking=True)
    indice = fields.Char('Indice',tracking=True,default='')
    designation= fields.Char('Designation',default='')
    hardness=fields.Selection([('easy','Easy'),('medium','Medium'),('hard','Hard')],default='easy',help='How its hard to manufacture this product')
    user_id=fields.Many2one('res.users','Responsable',tracking=True,ondelete='set null',help="responsable")
    create_date = fields.Datetime(string='Creation Date', readonly=True, index=True, help="Date on which cotation is created.")

    matieres = fields.One2many('we.cotation.material','cotation')
    # FROM we.product.template #
    time_study = fields.Float('Study Duration', digits=(16, 2), default=9.0,help="Time study duration  (in minutes)",tracking=True)
    cost_study = fields.Integer('Study Cost',default='60',help="Cost study",tracking=True)
    cost_administrative = fields.Integer('Administrative Cost',default='45',help="Cost administative",tracking=True)
    cost_tool = fields.Integer('Tool Cost',default='0',help="Cost of tools",tracking=True)
    material_margin = fields.Integer('Material Margin',default='35',help="Material margin (in percentage)",tracking=True)
    subcontracting_margin = fields.Integer('Subcontracting Margin',default='45',help="Subcontracting margin (in percentage)",tracking=True)
    note = fields.Char('Note',default='',tracking=True,help="Note")
    # //FROM we.product.template #
    @api.constrains('time_study')
    def _check_time_study(self):
        if any( record.time_study<0 for record in self):
            raise ValidationError(_('Time study must be greater than 0'))
    @api.constrains('cost_study')
    def _check_cost_study(self):
        if any( record.cost_study<0 for record in self):
            raise ValidationError(_('Cost study must be greater than 0'))
    @api.constrains('cost_administrative')
    def _check_cost_administrative(self):
        if any( record.cost_administrative<0 for record in self):
            raise ValidationError(_('Cost administrative must be greater than 0'))
    @api.constrains('cost_tool')
    def _check_cost_tool(self):
        if any( record.cost_tool<0 for record in self):
            raise ValidationError(_('Cost tool must be greater than 0'))
    @api.constrains('material_margin')
    def _check_material_margin(self):
        if any( record.material_margin<0 for record in self):
            raise ValidationError(_('Material margin must be greater than 0'))
    @api.constrains('subcontracting_margin')
    def _check_subcontracting_margin(self):
        if any( record.subcontracting_margin<0 for record in self):
            raise ValidationError(_('Subcontracting margin must be greater than 0'))

    