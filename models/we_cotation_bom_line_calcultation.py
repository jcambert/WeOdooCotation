from odoo import models, fields, api,_
from odoo.exceptions import AccessError, UserError,ValidationError
from .models import Model,models
from .res_config_settings import DIMENSION_ATTRIBUTE
class WeCotationBomLineCalculation(Model):
    _name='we.cotation.bom.line.calculation'
    _description = 'Helper that aids you calculate the good bom quantity'
    # _models={'attribute':'product.attribute','allowed_sheetmetal':'we.cotation.bom.line.calculation.allowed.sheetmetal'}
    #set default to True when calculation test maded
    bom_line=fields.Many2one('mrp.bom.line',string='Bom',required=False)
    type=fields.Selection([('sheetmetal','Sheetmetal'),('beam','Beam'),('operation','Operation')],default='sheetmetal',string='Type')

    formula=fields.Char('Formula')

    length=fields.Integer('Length',default=0)
    width=fields.Integer('Width',default=0)
    thickness=fields.Float('Thickness')
    quantity=fields.Integer('Quantity')
    material_name=fields.Char('Material name')
    material_volmass=fields.Float('Volumic mass')
    material_price=fields.Float('Material Price')
    allow_rot=fields.Boolean('90° rotation',default=True)

    piece_weight=fields.Float('Piece Weight',compute="_compute_best",store=True,readonly=True)
    piece_surface=fields.Float('Piece Surface',compute="_compute_best",store=True,readonly=True)
    piece_perimetre = fields.Float('Piece Perimetre',compute="_compute_best",store=True,readonly=True)

    total_piece_weight=fields.Float('Total Weight',compute="_compute_total",store=True,readonly=True)
    total_piece_surface=fields.Float('Total Surface',compute="_compute_total",store=True,readonly=True)

    unit_price=fields.Float('Unit Price',compute="_compute_amount",store=True,readonly=True)
    total_price=fields.Float('total Price',compute="_compute_amount",store=True,readonly=True)

    x_space=fields.Integer('X Space',default=10)
    y_space=fields.Integer('Y Space',default=10)

    left_sheetmetal_protection=fields.Integer('Left',default=0)
    right_sheetmetal_protection=fields.Integer('Right',default=0)
    top_sheetmetal_protection=fields.Integer('Top',default=0)
    bottom_sheetmetal_protection=fields.Integer('Bottom',default=0)

    best_length=fields.Float('Length',compute="_compute_best",store=True,readonly=True)
    best_width=fields.Float('Width',compute="_compute_best",store=True,readonly=True)
    best_sheetmetal_length=fields.Float('Sheetmetal length',compute="_compute_best",store=True,readonly=True)
    best_sheetmetal_width=fields.Float('Sheetmetal width',compute="_compute_best",store=True,readonly=True)
    best_sheetmetal_format=fields.Char('Sheetmetal Format',compute="_compute_format",readonly=True)
    best_piece_format=fields.Char('Piece Format',compute="_compute_format",readonly=True)

    qty_per_sheetmetal=fields.Integer('Quantity',compute="_compute_best",store=True,readonly=True)
    weight_per_piece=fields.Float('Weight',compute="_compute_best",store=True,readonly=True)
    percentage_loss=fields.Float('Percentage of loss',compute="_compute_best",store=True,readonly=True)

    allowed_sheetmetal_ids = fields.One2many('we.cotation.bom.line.calculation.allowed.sheetmetal','line_calculation',string='Alloweds')
    no_best=fields.Boolean('No best',compute="_compute_best",store=True,readonly=True)
    no_value=fields.Boolean(compute="_compute_best",readonly=True)

    def name_get(self):
        return [(record.id, '%s %sx%s' % (record.type, record.length,record.width ) ) for record in self]

    @api.model
    def default_get(self, vals):
        std_dims=self.attribute.browse( self.get_param(DIMENSION_ATTRIBUTE))
        
        default_sheetmetal=[]
        for std_dim in std_dims.value_ids:
            default_sheetmetal.append((0,0,{'length':std_dim.length,'width':std_dim.width }))
            default_sheetmetal.append((0,0,{'length':std_dim.width,'width':std_dim.length  }))
        res = super().default_get(vals)      
        res.update({'allowed_sheetmetal_ids':  default_sheetmetal})
        return res

    @api.constrains('length','width','thickness')
    def _check_dimension(self):
        if any( ((record.length<=0 or record.width<=0 or record.thickness<=0) and type in ['sheetmetal']) for record in self):
            raise ValidationError(_('The length or width must must be greater than zero when type is Sheetmetal'))

    @api.depends('length','width','thickness','material_volmass','x_space','y_space','left_sheetmetal_protection','right_sheetmetal_protection','top_sheetmetal_protection','bottom_sheetmetal_protection','allowed_sheetmetal_ids.available','allowed_sheetmetal_ids.length','allowed_sheetmetal_ids.width')
    def _compute_best(self):
        
        for record in self.filtered(lambda r:r.type in ['sheetmetal']):
            if record.length<=0 or record.width<=0 or record.thickness<=0:
                record.best_length=record.best_width=record.best_sheetmetal_length=record.best_sheetmetal_width=record.qty_per_sheetmetal=record.weight_per_piece=record.percentage_loss=record.piece_weight=record.piece_surface=0
                record.no_value=True
                record.no_best=True
                continue
            
            record.no_value=False
            """ Find the best format based on rectangular """
            best_percentage_loss=False
            best_id=False
            piece_surface=record.length*record.width
            record.piece_weight=(piece_surface*record.thickness*record.material_volmass)/1000000
            record.piece_surface=piece_surface*2
            record.piece_perimetre=(record.length+record.width)*2
            for std_dim in record.allowed_sheetmetal_ids.filtered(lambda r:r.available):
                
                cut_length=(std_dim.length-record.left_sheetmetal_protection-record.right_sheetmetal_protection)
                cut_width=(std_dim.width-record.top_sheetmetal_protection-record.bottom_sheetmetal_protection-record.y_space)

                nb_x=int(cut_length/(record.length+record.x_space))
                nb_y=int(cut_width/(record.width+record.y_space))

                nb=nb_x*nb_y
                if nb>0:
                    sheetmetal_surface=std_dim.length*std_dim.width
                    percentage_loss=(((sheetmetal_surface)-(piece_surface*nb)) / (sheetmetal_surface) if sheetmetal_surface>0 else 0)
                    std_dim.percentage_loss=percentage_loss
                    if not best_percentage_loss or best_percentage_loss>percentage_loss:
                        best_percentage_loss=percentage_loss
                        record.best_length=std_dim.length/nb_x 
                        record.best_width=std_dim.width/nb_y 
                        record.best_sheetmetal_length=std_dim.length
                        record.best_sheetmetal_width=std_dim.width
                        record.qty_per_sheetmetal=nb
                        record.weight_per_piece=(record.best_length*record.best_width*record.thickness*record.material_volmass)/1000000
                        record.percentage_loss=percentage_loss
                        best_id=std_dim.id
                        pass
            record.no_best= best_id==False
            for std_dim in record.allowed_sheetmetal_ids:
                std_dim.best= best_id==std_dim.id
    
    @api.depends('best_sheetmetal_length','best_sheetmetal_width')
    def _compute_format(self):
        filtered=self.filtered(lambda r:not r.no_best)
        for record in filtered:
            record.best_sheetmetal_format='%.2f x %.2f' % (record.length,record.width)
            record.best_piece_format='%.2f x %.2f' % (record.best_length,record.best_width)
        for record in self - filtered:
             record.best_sheetmetal_format= record.best_piece_format='' 

    @api.depends('quantity','piece_weight','piece_surface')
    def _compute_total(self):
        for record in self:
            record.total_piece_weight=record.quantity*record.piece_weight
            record.total_piece_surface=record.quantity*record.piece_surface
    
    @api.depends('material_price','piece_weight','quantity')
    def _compute_amount(self):
        for record in self:
            record.unit_price=record.material_price*record.piece_weight
            record.total_price=record.unit_price*record.quantity

    @api.onchange('allow_rot')
    def _on_allow_rot_changed(self):
        self.ensure_one()
        if self.allow_rot:
            return
        records=self.allowed_sheetmetal_ids.filtered(lambda r:r.length<r.width )
        records.map(lambda r:r.set_available(False))

    
class WeCotationBomLineCalculationAllowedSheetmetal(Model):
    _name='we.cotation.bom.line.calculation.allowed.sheetmetal'
    _description='Allowed sheetmal for a calculation'
    
    line_calculation=fields.Many2one('we.cotation.bom.line.calculation',string='Calculation')
    available=fields.Boolean('Available',default=True)
    length=fields.Integer('Length')
    width=fields.Integer('Width')
    percentage_loss=fields.Float('Loss',default=0.0)
    best=fields.Boolean('Best',readonly=True)

    @api.model
    def set_available(self,value=True):
        self.ensure_one()
        self.available=value
        return True

    @api.onchange('available')
    def _on_available_changed(self):
        for record in self:
            if record.length<record.width and record.available and not record.line_calculation.allow_rot:
                record.available=False
