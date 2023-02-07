from odoo import fields, models


class Employee(models.Model):
	_inherit = 'hr.employee'

	type_of_employee = fields.Selection(
        [('employee', 'Administration'), ('operator', 'Operation'), ('sale_marketing', 'Sales & Marketing')],
        string='Employee Type')
