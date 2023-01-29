from odoo import fields, models, api


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.model
    def validate_period_with_line_code(self, code):
        result = False
        if self.contract_id:
            for line in self.contract_id.contract_element_line_ids:
                if line.code == code:
                    result = line.validate_line_with_date_range(self.date_from, self.date_to)
        return result

    def compute_sheet(self):
        res = super().compute_sheet()
        self.validate_payslip_lines()
        return res

    def validate_payslip_lines(self):
        check_for_code = {}
        for each in self.contract_id.contract_element_line_ids:
            if each.from_date and each.to_date:
                check_for_code.update({
                    each.code: each
                    })
        for line in self.line_ids:
            if line.code in check_for_code:
                result = check_for_code[line.code].validate_line_with_date_range(self.date_from, self.date_to)
                if not result:
                    line.amount = 0.0
