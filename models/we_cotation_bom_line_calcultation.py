from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError
from .models import Model, models
from .res_config_settings import DIMENSION_ATTRIBUTE, UOM_SURFACE, UOM_WEIGHT, UOM_LENGTH, UOM_VOLUMIC_MASS

TYPE_SELECTION = [('sheetmetal', 'Sheetmetal'),
                  ('beam', 'Beam'), ('operation', 'Operation')]


class WeCotationBomLineCalculationTemplate(Model):
    _name = 'we.cotation.bom.line.calculation.template'
    _description = 'Line Template'

    def get_default_surface_domain(self):
        return [('category_id.id', '=', self.get_param(UOM_SURFACE))]

    def get_default_weight_domain(self):
        return [('category_id.id', '=', self.get_param(UOM_WEIGHT))]

    def get_default_length_domain(self):
        return [('category_id.id', '=', self.get_param(UOM_LENGTH))]

    active = fields.Boolean(default=True)
    name = fields.Char('name', required=True)
    sequence = fields.Integer('Sequence', default=1,
                              help="Used to order template")
    type = fields.Selection(
        TYPE_SELECTION, default='sheetmetal', string='Type')
    length = fields.Integer('Length', default=200)
    length_uom_id = fields.Many2one(
        'uom.uom', string='Length unit', required=True)
    width = fields.Integer('Width', default=100)
    width_uom_id = fields.Many2one(
        'uom.uom', string='Width unit', required=True)
    thickness = fields.Float('Thickness', default=0.0)
    thickness_uom_id = fields.Many2one(
        'uom.uom', string='Thickness unit', required=True)
    quantity = fields.Integer('Quantity', default=1)
    material_id = fields.Many2one(
        'we.material', string='Material ', required=True)
    allow_rot = fields.Boolean('90° rotation', default=True)

    x_space = fields.Integer('X Space', default=10)
    x_space_uom_id = fields.Many2one(
        'uom.uom', string='X gap unit', required=True)
    y_space = fields.Integer('Y Space', default=10)
    y_space_uom_id = fields.Many2one(
        'uom.uom', string='Y gap unit', required=True)

    left_sheetmetal_protection = fields.Integer('Left', default=0)
    left_sheetmetal_protection_uom_id = fields.Many2one(
        'uom.uom', string='Unity of measure', required=True)
    right_sheetmetal_protection = fields.Integer('Right', default=0)
    right_sheetmetal_protection_uom_id = fields.Many2one(
        'uom.uom', string='Unity of measure', required=True)
    top_sheetmetal_protection = fields.Integer('Top', default=0)
    top_sheetmetal_protection_uom_id = fields.Many2one(
        'uom.uom', string='Unity of measure', required=True)
    bottom_sheetmetal_protection = fields.Integer('Bottom', default=0)
    bottom_sheetmetal_protection_uom_id = fields.Many2one(
        'uom.uom', string='Unity of measure', required=True)

    piece_surface_uom_id = fields.Many2one('uom.uom', string='Surface unit', required=True, domain=lambda r: r.get_default_surface_domain())
    piece_weight_uom_id = fields.Many2one('uom.uom', string='Weight unit', required=True, domain=lambda r: r.get_default_weight_domain())
    piece_perimetre_uom_id = fields.Many2one('uom.uom', string='Surface unit', required=True, domain=lambda r: r.get_default_length_domain())
    best_piece_format_uom_id=fields.Many2one('uom.uom', string='Piece unit', required=True, domain=lambda r: r.get_default_length_domain())
    best_sheetmetal_format_uom_id=fields.Many2one('uom.uom', string='Sheetmetal unit', required=True, domain=lambda r: r.get_default_length_domain())
class WeCotationBomLineCalculation(Model):
    _name = 'we.cotation.bom.line.calculation'
    _inherit = ['base.uom.converter']
    _description = 'Helper that aids you calculate the good bom quantity'
    _models = {'attribute': 'product.attribute', 'allowed_sheetmetal': 'we.cotation.bom.line.calculation.allowed.sheetmetal',
               'material': 'we.material', 'template': 'we.cotation.bom.line.calculation.template'}
    # set default to True when calculation test maded

    def get_default_surface_domain(self):
        return [('category_id.id', '=', self.get_param(UOM_SURFACE))]

    def get_default_weight_domain(self):
        return [('category_id.id', '=', self.get_param(UOM_WEIGHT))]

    def get_default_length_domain(self):
        return [('category_id.id', '=', self.get_param(UOM_LENGTH))]

    def get_default_volumic_mass_domain(self):
        return [('category_id.id', '=', self.get_param(UOM_VOLUMIC_MASS))]

    tmpl_id = fields.Many2one(
        'we.cotation.bom.line.calculation.template', string='Template')
    bom_line = fields.Many2one('mrp.bom.line', string='Bom', required=False)
    sequence = fields.Integer('Sequence', default=1,
                              help="Used to order line.")
    type = fields.Selection(
        TYPE_SELECTION, default='sheetmetal', string='Type')

    length = fields.Float('Length', default=0)
    length_uom_id = fields.Many2one('uom.uom', string='Length unit', required=True, domain=lambda r: r.get_default_length_domain())
    width = fields.Float('Width', default=0)
    width_uom_id = fields.Many2one('uom.uom', string='Width unit',required=True, domain=lambda r: r.get_default_length_domain())
    thickness = fields.Float('Thickness')
    thickness_uom_id = fields.Many2one('uom.uom', string='Thickness unit', required=True, domain=lambda r: r.get_default_length_domain())
    quantity = fields.Float('Quantity')
    material_id = fields.Many2one('we.material', string='Material ', required=True)
    material_volmass = fields.Float('Volumic mass', related='material_id.volmass', readonly=True)
    material_volmass_uom_id = fields.Many2one('uom.uom', related='material_id.volmass_uom_id', readonly=True, domain=lambda r: r.get_default_volumic_mass_domain())
    material_unit_price = fields.Monetary('Material Price')
    material_price_uom_id = fields.Many2one('uom.uom', string='Unity of measure', required=True, domain=lambda r: r.get_default_weight_domain())
    allow_rot = fields.Boolean('90° rotation', default=True)

    piece_weight_uom_id = fields.Many2one('uom.uom', string='Weight unit', required=True, domain=lambda r: r.get_default_weight_domain())
    piece_surface_uom_id = fields.Many2one('uom.uom', string='Surface unit', required=True, domain=lambda r: r.get_default_surface_domain())
    piece_perimetre_uom_id = fields.Many2one('uom.uom', string='Perimeter unit', required=True, domain=lambda r: r.get_default_length_domain())

    piece_weight = fields.Float('Piece Weight', compute="_compute_best", store=True, readonly=True)
    piece_surface = fields.Float('Piece Surface', compute="_compute_best", store=True, readonly=True)
    piece_surface_painting = fields.Float('Piece Surface Painting', compute="_compute_best", store=True, readonly=True)
    piece_perimetre = fields.Float('Piece Perimetre', compute="_compute_best", store=True, readonly=True)

    total_piece_weight = fields.Float('Total Weight', compute="_compute_total", store=True, readonly=True)
    total_piece_surface = fields.Float('Total Surface', compute="_compute_total", store=True, readonly=True)
    total_piece_surface_painting = fields.Float('Total Surface painting', compute="_compute_total", store=True, readonly=True)

    currency_id = fields.Many2one('res.currency', string='Currency',required=True, default=lambda self: self.env.company.currency_id.id)
    unit_price = fields.Monetary('Unit Price', compute="_compute_amount", store=True, readonly=True)
    total_price = fields.Monetary('total Price', compute="_compute_amount", store=True, readonly=True)

    x_space = fields.Integer('X Space', default=10)
    x_space_uom_id = fields.Many2one('uom.uom', string='X gap unit', required=True, domain=lambda r: r.get_default_length_domain())
    y_space = fields.Integer('Y Space', default=10)
    y_space_uom_id = fields.Many2one('uom.uom', string='Y gap unit', required=True, domain=lambda r: r.get_default_length_domain())

    left_sheetmetal_protection = fields.Integer('Left', default=0)
    left_sheetmetal_protection_uom_id = fields.Many2one('uom.uom', string='Unity of measure', required=True, domain=lambda r: r.get_default_length_domain())
    right_sheetmetal_protection = fields.Integer('Right', default=0)
    right_sheetmetal_protection_uom_id = fields.Many2one('uom.uom', string='Unity of measure', required=True, domain=lambda r: r.get_default_length_domain())
    top_sheetmetal_protection = fields.Integer('Top', default=0)
    top_sheetmetal_protection_uom_id = fields.Many2one('uom.uom', string='Unity of measure', required=True, domain=lambda r: r.get_default_length_domain())
    bottom_sheetmetal_protection = fields.Integer('Bottom', default=0)
    bottom_sheetmetal_protection_uom_id = fields.Many2one('uom.uom', string='Unity of measure', required=True, domain=lambda r: r.get_default_length_domain())

    best_length = fields.Float('Length', compute="_compute_best", store=True, readonly=True)
    best_width = fields.Float('Width', compute="_compute_best", store=True, readonly=True)
    best_sheetmetal_length = fields.Float('Sheetmetal length', compute="_compute_best", store=True, readonly=True)
    best_sheetmetal_width = fields.Float('Sheetmetal width', compute="_compute_best", store=True, readonly=True)
    best_sheetmetal_format = fields.Char('Sheetmetal Format', compute="_compute_format", default="", readonly=True)
    best_sheetmetal_format_uom_id=fields.Many2one('uom.uom', string='Unity of measure', required=True, domain=lambda r: r.get_default_length_domain())
    best_piece_format = fields.Char('Piece Format', compute="_compute_format", default="", readonly=True)
    best_piece_format_uom_id=fields.Many2one('uom.uom', string='Unity of measure', required=True, domain=lambda r: r.get_default_length_domain())

    qty_per_sheetmetal = fields.Integer('Quantity', compute="_compute_best", store=True, readonly=True)
    weight_per_piece = fields.Float('Weight', compute="_compute_best", store=True, readonly=True)
    percentage_loss = fields.Float('Percentage of loss', compute="_compute_best", store=True, readonly=True)

    allowed_sheetmetal_ids = fields.One2many('we.cotation.bom.line.calculation.allowed.sheetmetal', 'line_calculation', string='Alloweds')
    no_best = fields.Boolean('No best', compute="_compute_best", default=False, store=True, readonly=True)
    no_value = fields.Boolean(compute="_compute_no_value", default=False, readonly=True)

    def name_get(self):
        return [(record.id, '%s %sx%s' % (record.type, record.length, record.width)) for record in self]

    @api.model
    def default_get(self, vals):

        std_dims = self.attribute.browse(self.get_param(DIMENSION_ATTRIBUTE))
        if not std_dims.uom_id:
            raise UserError(_('You must set UOM of dimension attribute'))
        tmpl = self.template.search([], limit=1)

        default_sheetmetal = []
        for std_dim in std_dims.value_ids:
            default_sheetmetal.append((0, 0, {'length': std_dim.length, 'width': std_dim.width, 'uom_id': std_dims.uom_id}))
            default_sheetmetal.append((0, 0, {'length': std_dim.width, 'width': std_dim.length, 'uom_id':std_dims.uom_id}))

        res = super().default_get(vals)
        data = {'allowed_sheetmetal_ids':  default_sheetmetal}
        res.update(data)

        data = {}
        if tmpl:
            data['tmpl_id'] = tmpl
        else:
            data['material_id'] = self.material.search([], limit=1)
        res.update(data)
        return res

    @api.constrains('length', 'width', 'thickness')
    def _check_dimension(self):
        if any(((record.length <= 0 or record.width <= 0 or record.thickness <= 0) and type in ['sheetmetal']) for record in self):
            raise ValidationError(
                _('The length or width must must be greater than zero when type is Sheetmetal'))

    @api.depends('length', 'width', 'thickness', 'material_volmass', 'x_space', 'y_space', 'left_sheetmetal_protection', 'right_sheetmetal_protection', 'top_sheetmetal_protection', 'bottom_sheetmetal_protection', 'allowed_sheetmetal_ids.available', 'allowed_sheetmetal_ids.length', 'allowed_sheetmetal_ids.width')
    def _compute_best(self):

        for record in self.filtered(lambda r: r.type in ['sheetmetal']):
            record.compute_best()

    @api.model
    def compute_best(self):
        self.ensure_one()
        record = self
        if(record.type != 'sheetmetal'):
            return
        if record.length <= 0 or record.width <= 0 or record.thickness <= 0:
            record.best_length = record.best_width = record.best_sheetmetal_length = record.best_sheetmetal_width = record.qty_per_sheetmetal = record.weight_per_piece = record.percentage_loss = record.piece_weight = record.piece_surface = record.piece_surface_painting = 0
            record.no_value = True
            record.no_best = True
            return

        record.no_value = False
        """ Find the best format based on rectangular """
        record.calculate_surface_and_weight()

        availables = record.allowed_sheetmetal_ids.filtered(
            lambda r: r.available)
        for std_dim in (record.allowed_sheetmetal_ids-availables):
            std_dim.percentage_loss = percentage_loss = 1

        values=[]
        std_dims = self.attribute.browse(self.get_param(DIMENSION_ATTRIBUTE))
        for std_dim in availables:
            std_dim.uom_id=std_dims.uom_id
            cut_length = std_dim.get_base_length()-record.left_sheetmetal_protection_uom_id.convert_to_base(record.left_sheetmetal_protection) - \
                record.right_sheetmetal_protection_uom_id.convert_to_base(
                    record.right_sheetmetal_protection)
            cut_width = std_dim.get_base_width()-record.top_sheetmetal_protection_uom_id.convert_to_base(record.top_sheetmetal_protection) - \
                record.bottom_sheetmetal_protection_uom_id.convert_to_base(
                    record.bottom_sheetmetal_protection)-record.y_space_uom_id.convert_to_base(record.y_space)

            _length = record.length_uom_id.convert_to_base(
                record.length)+record.x_space_uom_id.convert_to_base(record.x_space)
            _width = record.width_uom_id.convert_to_base(
                record.width)+record.y_space_uom_id.convert_to_base(record.y_space)

            if _length<= 0 or _width<=0:
                continue
            nb_x = int(cut_length/_length)
            nb_y = int(cut_width/_width)
            nb = nb_x*nb_y
            # if nb>0:
            sheetmetal_surface = std_dim.get_base_surface()
            percentage_loss = (((sheetmetal_surface)-(_length*_width*nb)) /
                               (sheetmetal_surface) if sheetmetal_surface > 0 else 1)
            # std_dim.nb_x = nb_x
            # std_dim.nb_y = nb_y
            
            # std_dim.percentage_loss = percentage_loss
            values.append((1,std_dim.id,{'nb_x':nb_x,'nb_y':nb_y,'percentage_loss':percentage_loss}))
            std_dim.write({'nb_x':nb_x,'nb_y':nb_y,'percentage_loss':percentage_loss})
        # record.write({'allowed_sheetmetal_ids':  values})
    # @api.depends('allowed_sheetmetal_ids.percentage_loss')
    # def _compute_best_sheetmetal_format(self):
        # for record in self:
        first = True
        record.best_length = record.best_width = record.best_sheetmetal_length = record.best_sheetmetal_width = record.qty_per_sheetmetal = record.weight_per_piece = record.percentage_loss = 0
        record.no_best = True
        for std_dim in record.allowed_sheetmetal_ids.sorted(lambda r: r.percentage_loss):
            if first:
                first = False
                if std_dim.nb_x<=0 or std_dim.nb_y<=0:
                    continue
                record.best_length = record.get_base_length()._compute_quantity(std_dim.get_base_length()/std_dim.nb_x, record.length_uom_id)
                record.best_width = record.get_base_length()._compute_quantity(std_dim.get_base_width()/std_dim.nb_y, record.width_uom_id)
                record.best_sheetmetal_length = std_dim.length
                record.best_sheetmetal_width = std_dim.width
                record.qty_per_sheetmetal = std_dim.nb_x*std_dim.nb_y
                record.weight_per_piece = record.calculate_weight(record.best_length, record.length_uom_id, record.best_width, record.width_uom_id,record.thickness, record.thickness_uom_id, record.material_id.volmass, record.material_id.volmass_uom_id, record.piece_weight_uom_id)
                record.percentage_loss = std_dim.percentage_loss
                std_dim.best = True
                record.no_best = False
                continue

            std_dim.best = False

    @api.model
    def calculate_perimeter(self, length, length_uom, width, width_uom, uom_id):
        base_length = self.get_base_length()
        _length = length_uom.convert_to_base(length)
        _width = width_uom.convert_to_base(width)
        _perimeter = base_length._compute_quantity((_length+_width)*2, uom_id)
        return _perimeter

    @api.model
    def calculate_surface(self, length, length_uom, width, width_uom, surface_uom):
        base_surface = self.get_base_surface()
        _length = length_uom.convert_to_base(length)
        _width = width_uom.convert_to_base(width)

        _surface = base_surface._compute_quantity(_length*_width, surface_uom)
        return _surface

    @api.model
    def calculate_weight(self, length, length_uom, width, width_uom, thickness, thickness_uom, volmass, volmass_uom, weight_uom):
        base_weight = self.get_base_weight()
        _length = length_uom.convert_to_base(length)
        _width = width_uom.convert_to_base(width)
        _thickness = thickness_uom.convert_to_base(thickness)
        _volmass = volmass_uom.convert_to_base(volmass)

        _weight = base_weight._compute_quantity(_length*_width*_thickness*_volmass, weight_uom)
        return _weight

    @api.model
    def calculate_surface_and_weight(self):
        self.ensure_one()
        record = self

        _perimeter = record.calculate_perimeter(record.length, record.length_uom_id, record.width, record.width_uom_id, record.piece_perimetre_uom_id)
        _surface = record.calculate_surface(record.length, record.length_uom_id, record.width, record.width_uom_id, record.piece_surface_uom_id)
        _weight = record.calculate_weight(record.length, record.length_uom_id, record.width, record.width_uom_id, record.thickness,record.thickness_uom_id, record.material_id.volmass, record.material_id.volmass_uom_id, record.piece_weight_uom_id)

        record.piece_perimetre = _perimeter
        record.piece_surface = _surface
        record.piece_surface_painting = _surface*2
        record.piece_weight = _weight

        record.weight_per_piece = record.calculate_weight(record.best_length, record.length_uom_id, record.best_width, record.width_uom_id,record.thickness, record.thickness_uom_id, record.material_id.volmass, record.material_id.volmass_uom_id, record.piece_weight_uom_id)


    @api.onchange('piece_perimetre_uom_id','length','length_uom_id','width','width_uom_id')
    def _on_piece_perimetre_uom_id_changed(self):
        for record in self:
            _perimeter = record.calculate_perimeter(record.length, record.length_uom_id, record.width, record.width_uom_id, record.piece_perimetre_uom_id)
            record.update({'piece_perimetre':_perimeter})

    @api.onchange( 'piece_surface_uom_id','length','length_uom_id','width','width_uom_id')
    def _on_piece_surface_uom_id_changed(self):
        for record in self:
            _surface = record.calculate_surface(record.length, record.length_uom_id, record.width, record.width_uom_id, record.piece_surface_uom_id)
            record.write({'piece_surface':_surface,'piece_surface_painting':_surface*2})
    @api.onchange('piece_weight_uom_id','length','length_uom_id','width','width_uom_id','thickness','thickness_uom_id','volmass')
    def _on_piece_weight_uom_id_changed(self):
        for record in self:
            _weight = record.calculate_weight(record.length, record.length_uom_id, record.width, record.width_uom_id, record.thickness,record.thickness_uom_id, record.material_id.volmass, record.material_id.volmass_uom_id, record.piece_weight_uom_id)
            _weight_per_piece = record.calculate_weight(record.best_length, record.length_uom_id, record.best_width, record.width_uom_id,record.thickness, record.thickness_uom_id, record.material_id.volmass, record.material_id.volmass_uom_id, record.piece_weight_uom_id)
            record.write({'piece_weight':_weight,'weight_per_piece':_weight_per_piece}) 
    @api.depends('length', 'width', 'thickness')
    def _compute_no_value(self):
        for record in self:
            record.no_value = record.length <= 0 or record.width <= 0 or record.thickness <= 0

    @api.depends('best_sheetmetal_length', 'best_sheetmetal_width')
    def _compute_format(self):
        records = self.filtered(lambda r: not r.no_best)
        for record in records:
            best=record.allowed_sheetmetal_ids.search([('best','=',True)],limit=1)
            if best:
                _length=best.uom_id._compute_quantity(record.best_sheetmetal_length,record.best_sheetmetal_format_uom_id)
                _width=best.uom_id._compute_quantity(record.best_sheetmetal_width,record.best_sheetmetal_format_uom_id)
                record.best_sheetmetal_format = '%.2f %s x %.2f %s' % (_length,record.best_sheetmetal_format_uom_id.display_name, _width,record.best_sheetmetal_format_uom_id.display_name)
            if record.best_piece_format_uom_id:
                _length=record.length_uom_id._compute_quantity(record.best_length,record.best_piece_format_uom_id)
                _width=record.width_uom_id._compute_quantity(record.best_width,record.best_piece_format_uom_id)
                record.best_piece_format = '%.2f %s x %.2f %s' % (record.best_length,record.best_piece_format_uom_id.display_name, record.best_width,record.best_piece_format_uom_id.display_name)
            else:
                record.best_piece_format = ''

        for record in (self - records):
            record.best_sheetmetal_format = record.best_piece_format = ''

    @api.depends('quantity', 'piece_weight', 'piece_surface')
    def _compute_total(self):
        for record in self:
            record.total_piece_weight = record.quantity*record.piece_weight
            record.total_piece_surface = record.quantity*record.piece_surface
            record.total_piece_surface_painting = record.quantity*record.piece_surface_painting

    @api.depends('material_unit_price', 'piece_weight', 'quantity')
    def _compute_amount(self):
        for record in self:
            record.unit_price = record.material_unit_price*record.piece_weight
            record.total_price = record.unit_price*record.quantity

    @api.onchange('tmpl_id')
    def _on_tmpl_id_changed(self):
        ignore_fields = ('id', 'sequence', 'active', 'name')
        for record in self:
            fields = (
                field for field in record.tmpl_id._fields if field not in ignore_fields)
            for field in fields:
                record[field] = record.tmpl_id[field]

            record._compute_best()

    @api.onchange('material_id')
    def _on_material_id_changed(self):
        for record in self:
            record.material_unit_price = record.material_id.unit_price
            record.material_price_uom_id = record.material_id.price_uom_id

    @api.onchange('allow_rot')
    def _on_allow_rot_changed(self):
        self.ensure_one()
        if self.allow_rot:
            return
        records = self.allowed_sheetmetal_ids.filtered(
            lambda r: r.length < r.width)
        for record in records:
            # records.map(lambda r:r.set_available(False))
            record.set_available(False)


class WeCotationBomLineCalculationAllowedSheetmetal(Model):
    _name = 'we.cotation.bom.line.calculation.allowed.sheetmetal'
    _description = 'Allowed sheetmal for a calculation'

    line_calculation = fields.Many2one('we.cotation.bom.line.calculation', string='Calculation')
    available = fields.Boolean('Available', default=True)
    length = fields.Integer('Length')
    width = fields.Integer('Width')

    uom_id = fields.Many2one('uom.uom', string='Length unit')
    percentage_loss = fields.Float('Loss', default=0.0)
    best = fields.Boolean('Best')

    nb_x = fields.Integer('Nb X')
    nb_y = fields.Integer('Nb Y')
    qty_per_sheetmetal = fields.Integer(
        'Quantity', compute="_compute_qty")

    @api.model
    def set_available(self, value=True):
        self.ensure_one()
        self.available = value
        return True
    @api.depends('nb_x','nb_y')
    def _compute_qty(self):
        for record in self:
            record.qty_per_sheetmetal=record.nb_x*record.nb_y

    @api.onchange('available')
    def _on_available_changed(self):
        for record in self:
            if record.length < record.width and not record.line_calculation.allow_rot:
                record.available = False
                raise UserError(_('Rotation is not enabled'))

    @api.model
    def get_base_surface(self):
        self.ensure_one()
        return self.get_base_length() * self.get_base_width()

    @api.model
    def get_base_length(self):
        self.ensure_one()
        return self.uom_id.convert_to_base(self.length)

    @api.model
    def get_base_width(self):
        self.ensure_one()
        return self.uom_id.convert_to_base(self.width)
  