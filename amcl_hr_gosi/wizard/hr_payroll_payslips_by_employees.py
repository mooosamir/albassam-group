# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    def compute_sheet(self):
        for payslip in self:
            res = super(HrPayslipEmployees, payslip).compute_sheet()
            context = dict(payslip.env.context)
            active_id = payslip.env['hr.payslip.run'].browse(context.get('active_id'))
            if active_id:
                for slip in active_id.slip_ids:
                    slip_data = payslip.env['hr.payslip'].onchange_employee_id(active_id.date_start, active_id.date_end, slip.employee_id.id, contract_id=False)
                    slip.gosi_id = slip_data['value'].get('gosi_id')
            return res

