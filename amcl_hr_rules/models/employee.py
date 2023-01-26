from odoo import fields, models


class Employee(models.Model):
	_inherit = 'hr.employee'

	type_of_employee = fields.Selection(
        [('employee', 'Employee'), ('operator', 'Operation')],
        string='Employee Type', default='employee')
