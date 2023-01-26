from odoo import models, fields


class HrContractElements(models.Model):
	_name = 'hr.contract.elements'
	_description = "Contract Elements"

	name = fields.Char(string="Name", required=True)
	calculation_type = fields.Selection([('value','Value'),('percentage','Percentage')],string="Calculation Type")
	percentage = fields.Integer(string="Percentage")