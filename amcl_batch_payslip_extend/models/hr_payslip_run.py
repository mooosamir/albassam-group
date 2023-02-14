from odoo import fields, models


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    def write(self, vals):
        res = super().write(vals)
        if self.state == 'verify':
            for payslip in self.slip_ids:
                payslip._compute_worked_days_line_ids()
        return res
