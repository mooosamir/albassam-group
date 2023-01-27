from odoo import fields, models, api


class ContractElementLine(models.Model):
    _name = 'hr.contract.element.line'
    _description = 'Hr Contract Element Line'

    contract_elem_conf_id = fields.Many2one('hr.contract.element.config', string='Contract Element', required=True)
    code = fields.Char(related='contract_elem_conf_id.code', string='Code')
    is_basic = fields.Boolean(related='contract_elem_conf_id.is_basic', string='Is Basic')
    calculation_type = fields.Selection(related='contract_elem_conf_id.calculation_type', string='Calculation Type')# [('value','Value'),('percentage','Percentage')]
    amount = fields.Monetary(string='Amount', required=True, tracking=True)
    from_date = fields.Date(string='From')
    to_date = fields.Date(string='To')


    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', compute='_compute_employee_contract')
    contract_id = fields.Many2one('hr.contract', string='Contract')

    @api.depends('contract_id')
    def _compute_employee_contract(self):
        for each in self:
            if each.contract_id:
                each.company_id = each.contract_id.employee_id.company_id.id

    @api.onchange('contract_elem_conf_id')
    def onchange_contract_elem_conf_id(self):
        amount = 0
        if self.contract_elem_conf_id.calculation_type == 'percentage':
            required_line_id = self.contract_id.get_element_line(self.contract_elem_conf_id.percentage_of_id)
            amount = (required_line_id.amount * self.contract_elem_conf_id.percentage) / 100
        self.amount = amount
