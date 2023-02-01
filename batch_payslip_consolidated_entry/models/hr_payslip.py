# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrPayslipExtend(models.Model):
    _inherit = 'hr.payslip'

    # def action_payslip_done(self):
    #     """
    #         Generate the accounting entries related to the selected payslips
    #         A move is created for each journal and for each month.
    #     """
    #     res = super(HrPayslipExtend, self).action_payslip_done()
    #     if self.payslip_run_id:
    #         if self.payslip_run_id.group_by_analytic_account:
    #             self._action_create_consolidated_entry()
    #         else:
    #             self._action_create_account_move()
    #     else:
    #         self._action_create_account_move()
    #     return res
    #
    # def _action_create_consolidated_entry(self):
    #     print('Hello')
