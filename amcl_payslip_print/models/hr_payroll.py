# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from num2words import num2words


class HRPayslip(models.Model):
    _inherit = "hr.payslip"

    def print_payslip_report(self):
        report_id = self.env.ref('amcl_payslip_print.amcl_custom_payslip_report')
        return report_id.report_action(self)

    def action_print_payslip(self):
        return self.print_payslip_report()

    def get_joining_date(self, date):
        joining_date = ''
        if date:
            joining_date = date.strftime("%d/%m/%Y")
        return joining_date

    def get_working_days(self):
        number_of_days = [line.number_of_days for line in self.worked_days_line_ids]
        working_days = int(sum(number_of_days))
        return working_days

    def get_earning_lines(self):
        earning_lines = []
        for line in self.line_ids:
            if line.amount > 0:
                earning_lines.append(line.read(['name','amount','total'])[0])
        return earning_lines

    def get_deduction_lines(self):
        deduction_lines = []
        for line in self.line_ids:
            if line.amount < 0 and line.salary_rule_id.appears_on_payslip and line.salary_rule_id.code not in ['GOSI-Company-Contribution-Non-Saudi-Employee', 'GOSI-Company-Contribution-Saudi-Employee']:
                deduction_lines.append(line.read(['name','total'])[0])
        return deduction_lines

    def get_total_amount_in_words(self, amount):
        return num2words(amount)

    def get_total_earning_amount(self):
        total_earning_amount = 0
        for line in self.line_ids:
            if line.salary_rule_id.code == 'NET':
                total_earning_amount += line.amount
        return total_earning_amount

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
