from odoo import models, fields, api


class HrContractElementConfig(models.Model):
    _name = 'hr.contract.element.config'
    _description = 'Contract Element Config'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    is_basic = fields.Boolean(string='Is Basic')
    calculation_type = fields.Selection([('value','Value'),('percentage','Percentage')],string='Calculation Type', required=True)
    percentage = fields.Integer(string='Percentage(%)')
    percentage_of_id = fields.Many2one('hr.contract.element.config', string='Percentage Of', domain=[('calculation_type','=','value')])

    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.company)
