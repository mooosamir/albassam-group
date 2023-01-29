# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    group_by_analytic_account = fields.Boolean('Group By Analytic Account')


