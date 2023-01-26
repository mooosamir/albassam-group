from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

selection_data = [
    ('regular', 'Regular','timesheet_type'),
    ('overtime', 'Overtime','timesheet_type'),
]

def _get_selections(name):
   data = filter(lambda x: x[2] == name, selection_data)
   return list(map(lambda x: (x[0], x[1]), data))


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    timesheet_type = fields.Selection(lambda self: _get_selections('timesheet_type'), string='Type', default='regular', required=True)

    @api.model
    def create(self, vals):
        if 'unit_amount' in vals:
            self.with_context(from_create=True).validate_hours_spent(vals)
        res = super().create(vals)
        return res

    def write(self, vals):
        if 'unit_amount' in vals:
            self.validate_hours_spent(vals)
        res = super().write(vals)
        return res
    
    @api.model
    def validate_hours_spent(self, vals):
        timesheet_type = False
        if self._context.get('from_create', False):
            timesheet_type = vals.get('timesheet_type')
            unit_amount = vals.get('unit_amount')
        else:
            timesheet_type = vals.get('timesheet_type',self.timesheet_type)
            unit_amount = vals.get('unit_amount')
        if timesheet_type == 'regular':
            if unit_amount > 12:
                raise ValidationError(_("Hours spent can not be more than 12 hours."))
        if timesheet_type == 'overtime':
            if unit_amount > 4:
                raise ValidationError(_("Hours spent for Overtime can not be more than 4 hours."))
