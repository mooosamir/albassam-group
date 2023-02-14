# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import models, fields, api 
from odoo.osv import expression


class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    exclude_department_ids = fields.Many2many('hr.department', 'batch_emp_wizard_department_rel', 'batch_wizard_id', 'department_id', string='Exclude Department')

    @api.depends('exclude_department_ids')
    def _compute_employee_ids(self):
        res = super()._compute_employee_ids()
        for wizard in self:
            domain = wizard._get_available_contracts_domain()
            if wizard.exclude_department_ids:
                department_ids = self.env['hr.department'].search([('id', 'child_of', self.exclude_department_ids.ids)])
                domain = expression.AND([
                    domain,
                    [('department_id', 'not in', department_ids.ids)]
                ])
            wizard.employee_ids = self.env['hr.employee'].search(domain)
        return res
