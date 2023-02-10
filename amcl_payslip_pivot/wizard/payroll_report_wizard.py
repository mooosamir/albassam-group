from odoo import fields, models, api


class PayrollReportWizard(models.TransientModel):
    _name = 'payroll.report.wizard'
    _description = 'Payroll Report Wizard'

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    company_ids = fields.Many2many('res.company', 'payroll_pivot_report_company_rel', 'payroll_report_wizard_id', 'company_id', string='Company')

    def open_payroll_pivot_view(self):
        action_id = self.sudo().env.ref('amcl_payslip_pivot.action_payslip_custom_report').read()[0]
        ctx = self.env.context.copy()
        ctx.update({'wizard_id': self.id})
        self.env['hr.payroll.custom.report'].with_context(ctx).init()
        return action_id

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        print (self._context.get('allowed_company_ids'))
        res.update({
            'company_ids': [(4,self.env.company.id)]
            })
        return res
