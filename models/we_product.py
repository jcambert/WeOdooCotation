# -*- coding: utf-8 -*-

from odoo import models, fields,tools, api,_
from odoo.exceptions import AccessError, UserError,ValidationError

class Product(models.Model):
    _inherit = ['product.template']
    _description = 'Product Quotation Extensions'

    quotation_count = fields.Integer('Quotation',compute='_compute_quotation_count')

    @api.depends('name')
    def _compute_quotation_count(self):
        for record in self.filtered(lambda r:r.sale_ok):
            record.quotation_count= self.env['we.cotation.product'].search_count([('name','=',record.name)])
        for record in self.filtered(lambda r:not r.sale_ok):
            record.quotation_count=0
    def action_create_quotation(self):
        pass
    def action_view_quotations(self):
        pass


class WeProduct(models.Model):
    """ Model for cotation processing
    """
    _inherit = ['we.cotation.product.template']
    _name='we.cotation.product'
    _description='Cotation Products'
    _order = "name"
    _sql_constraints = [
        ('we_cotation_product_name_uniq', 'unique (name,revision)', "The number/revision already exist!"),
    ]
    @tools.ormcache()
    def _get_default_uom_id(self):
        return self.env.ref('uom.product_uom_unit')
    active = fields.Boolean(default=True,tracking=True)
    cotation=fields.Many2one('we.cotation','Cotation')
    name = fields.Char('Product Name', default='',required=True, tracking=True)
    indice = fields.Char('Indice',tracking=True,default='')
    designation= fields.Char('Designation',tracking=True,default='')
    uom_id = fields.Many2one('uom.uom', 'Unit of Measure',default=_get_default_uom_id, required=True,help="Default unit of measure used for all stock operations.")
    uom_name = fields.Char(string='Unit of Measure Name', related='uom_id.name', readonly=True)
    hardness=fields.Selection([('easy','Easy'),('medium','Medium'),('hard','Hard')],default='easy',tracking=True,help='How its hard to manufacture this product')
    deviser_id=fields.Many2one('res.users','Responsable',tracking=True,ondelete='set null',help="responsable")
    create_date = fields.Datetime(string='Creation Date', readonly=True, index=True, help="Date on which cotation is created.")

    matieres = fields.One2many('we.cotation.material','cotation')
    
    bom_lines = fields.One2many('we.cotation.bom.line', 'product', 'BoM Components')
    boms = fields.One2many('we.cotation.bom', 'product', 'Bill of Materials')
    bom_count = fields.Integer('# Bill of Material',compute='_compute_bom_count', compute_sudo=False)
    used_in_bom_count = fields.Integer('# of BoM Where is Used', compute='_compute_used_in_bom_count', compute_sudo=False)
    # components = fields.Many2many('we.cotation.product','we_cotation_product_rel','product_parent_id','product_child_id',tracking=True,string='Components')
    # operations = fields.Many2one('we.cotation.operation',string='Operations')

    material_cost = fields.Float('Material cost',digits=(16, 2), default='0.0',help='price per unit')
    component_cost = fields.Float('Component cost',digits=(16, 2), default='0.0',help='price per unit',store=True,compute='_compute_component_cost')
    preparation_cost = fields.Float('Preparation cost',digits=(16, 2), default='0.0',help='price per unit')
    mo_cost = fields.Float('Mo cost',digits=(16, 2), default='0.0',help='price per unit')

    @api.model
    def default_get(self, fields):
        defaults = super(WeProduct, self).default_get(fields)
        defaults['deviser_id']=self.env.user
        tpl=self.env['we.cotation.product.template'].search([('active','=',True)],limit=1)

        if tpl:
            defaults['time_study']=tpl.time_study
            defaults['cost_study']=tpl.cost_study
            defaults['cost_administrative']=tpl.cost_administrative
            defaults['cost_tool']=tpl.cost_tool
            defaults['material_margin']=tpl.material_margin
            defaults['subcontracting_margin']=tpl.subcontracting_margin
            defaults['note']=tpl.note
        return defaults
    # @api.depends('components')
    # def _compute_component_cost(self):
    #     for record in self:
    #         for cmp in record.components:
    #             record.component_cost+=cmp.component_cost
    
    def _compute_bom_count(self):
        for product in self:
            product.bom_count = self.env['we.cotation.bom'].search_count([('product', '=', product.id)])
    def _compute_used_in_bom_count(self):
        for record in self:
            record.used_in_bom_count = self.env['we.cotation.bom'].search_count([('bom_lines.product', 'in', record.product.ids)])