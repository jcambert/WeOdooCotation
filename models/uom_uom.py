from odoo.exceptions import AccessError, UserError
from odoo import models, fields, api, _
from .models import Model



class WeUom(Model):
    _inherit='uom.uom'
    _models={'uom':'uom.uom'}

    @api.model
    def get_base(self):
        self.ensure_one()
        return self.uom.search([('category_id.id','=',self.category_id.id),('uom_type','=','reference')],limit=1)

    def convert_to_base(self,qty, rounding=False, rounding_method='UP', raise_if_failure=True):
        if not self.id:
            return 0.0
        uom_base=self.get_base()
        return self._compute_quantity(qty,uom_base,rounding,rounding_method,raise_if_failure)