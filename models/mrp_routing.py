from odoo.exceptions import AccessError, UserError
from odoo import models, fields, api, _

class MrpRoutingWorkcenter(models.Model):
    _inherit='mrp.routing.workcenter'

    time_cycle_prep = fields.Float('Preparation Duration',default=0.0)


    @api.onchange('workcenter_id')
    def _on_workcenter_changed(self):
        self.time_cycle_prep = self.time_cycle_prep if self.time_cycle_prep>0 else self.workcenter_id.time_cycle_prep
