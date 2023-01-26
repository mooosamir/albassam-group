from odoo import models, fields


class ResCompany(models.Model):
	_inherit = 'res.company'

	company_code = fields.Char(string="Code")

	_sql_constraints = [
        ('company_code_uniq', 'unique (company_code)', 'The company code must be unique !')
    ]