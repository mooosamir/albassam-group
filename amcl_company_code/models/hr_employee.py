from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Employee(models.Model):
    _inherit = 'hr.employee'

    employee_sequence = fields.Char(string='Employee ID', readonly= True)

    _sql_constraints = [
        ('emp_seqence_uniq', 'unique (employee_sequence)', 'The employee sequence must be unique !')
    ]

    @api.model
    def create(self, vals):
        if not vals.get('employee_sequence', False):
            if self.env.company.company_code:
                employee_no = self.env['ir.sequence'].next_by_code('employee_seq')
                company_code = self.env.company.company_code
                employee_id = company_code + employee_no
                vals['employee_sequence'] = employee_id
            else:
                raise ValidationError('Please enter your Company code first.')
        return super().create(vals)
        
