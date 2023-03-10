# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class NewJoiningEmployee(models.AbstractModel):
    _name = 'report.amcl_hr.report_new_joining_employee'

    @api.model
    def get_report_values(self, doc_ids, data=None):
        if not data.get('id') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        employees = self.env['hr.employee'].search([('joining_date', '>=', data['start_date']),
                                                    ('joining_date', '<=', data['end_date'])])
        return {
            'doc_ids': self.ids,
            'doc_model': model,
            'data': data,
            'docs': docs,
            'employees': employees,
        }
