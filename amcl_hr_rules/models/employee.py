from odoo import fields, models


class Employee(models.Model):
	_inherit = 'hr.employee'

	type_of_employee = fields.Selection(
        [('employee', 'Employee'), ('operator', 'Operation'), ('sale_marketing', 'Sales & Marketing')],
        string='Administration')
