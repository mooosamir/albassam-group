from odoo import fields, models


class ContractAmendment(models.Model):
    _inherit = 'contract.amendment'

    contract_amendment_package_ids = fields.One2many('contract.package.config.line', 'amendment_id', 'Contract Amendments', track_visibility='onchange')

    def action_amendment_done(self):
        self.ensure_one()
        self.employee_id.department_id = self.new_department_id.id or False
        self.employee_id.job_id = self.new_job_id.id or False
        self.hr_contract_id.date_start = self.current_start_date or False
        self.hr_contract_id.date_end = self.current_end_date or False

        for amendment_line in self.contract_amendment_package_ids:
            contract_elem_line_id = self.get_elem_line(amendment_line.contract_elem_conf_id)
            if contract_elem_line_id:
                contract_elem_line_id.write({
                    'amount': amendment_line.new_package
                    })
            else:
                self.env['hr.contract.element.line'].create({
                    'contract_id': self.hr_contract_id.id,
                    'contract_elem_conf_id': amendment_line.contract_elem_conf_id.id,
                    'amount': amendment_line.new_package,
                    })
            amendment_line.approved_date = fields.Date.today()
        self.write({'state': 'done'})

    def get_elem_line(self, contract_elem_conf_id):
        for line in self.hr_contract_id.contract_element_line_ids:
            if line.contract_elem_conf_id.id == contract_elem_conf_id.id:
                return line
        return False
