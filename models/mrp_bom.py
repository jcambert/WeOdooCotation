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

class WeCotation(models.Model):
    _name='we.cotation'
    _description='Quotation'
    _inherit=['mail.activity.mixin','mail.thread']
    _sql_constraints = [
        ('we_cotation_cotation_name_uniq', 'unique (number,revision)', "The number/revision already exist!"),
    ]
    active = fields.Boolean(default=True)
    number = fields.Char('Number',required=True, index=True, tracking=True,copy=False)
    revision = fields.Char('Revision',index=True, tracking=True,copy=False)
    bom_ids = fields.One2many('mrp.bom','quotation_id',string='Boms')
    deviser_id=fields.Many2one('res.users','Deviseur',ondelete='set null',help="Deviseur")
    responsable_id=fields.Many2one('res.users','Responsable',ondelete='set null',help="Responsable")
    stage_id=fields.Many2one('we.cotation.stage',
        ondelete='restrict',
        help="Stage",
        compute='_compute_stage_id',
        group_expand='_read_group_stage_names',
        index=True, tracking=True,copy=False,readonly=False, store=True
        )
    color = fields.Integer('Couleur')
    bom_ids = fields.One2many('mrp.bom','quotation_id',string='Bom')

    
    def name_get(self):
        return [(record.id, '%s Révision:%s' % (record.number, record.revision ) ) if record.revision else (record.id, record.number) for record in self]

    @api.model
    def default_get(self, fields):
        defaults = super(WeCotation, self).default_get(fields)
        defaults['deviser_id']=self.env.user
        return defaults
    def _read_group_stage_names(self, stages, domain, order):
        search_domain=[]
        stages_ids = stages.search(search_domain)
        return stages_ids
    def _compute_stage_id(self):
        for record in self.filtered(lambda r: not r.stage_id):
            record.stage_id = record._stage_find(domain=[('fold', '=', False)]).id

class WeBom(models.Model):
    _inherit='mrp.bom'

    type = fields.Selection(selection_add=[('quot','Quotation')], ondelete={'quot': 'cascade'})
    quotation_id = fields.Many2one('we.cotation',string='Quotation')

    @api.constrains('type','quotation_id')
    def _check_quotation(self):
        if any(bom.type=='quot' and not bom.quotation_id for bom in self ):
            raise UserError(_('Quotation must be selected'))

class WeBomLine(models.Model):
    _inherit = 'mrp.bom.line'

