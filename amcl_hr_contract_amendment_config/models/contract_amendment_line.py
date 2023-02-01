from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ContractAmendmentConfigLine(models.Model):
    _name = 'contract.package.config.line'
    _description = 'Contract Amendment Config Line'

    amendment_id = fields.Many2one('contract.amendment', 'Amendment', required=True)
    contract_elem_conf_id = fields.Many2one('hr.contract.element.config', string='Contract Element', required=True, domain=[('calculation_type','not in', ['percentage'])])
    current_package = fields.Float('Current Package')
    change_value = fields.Float('Increment/Decrement Value', required=True)
    new_package = fields.Float('New Package',compute='_compute_new_package', required=True)
    state = fields.Selection(related='amendment_id.state', store=True)
    employee_id = fields.Many2one('hr.employee', related='amendment_id.employee_id', store=True)
    hr_contract_id = fields.Many2one('hr.contract', related='amendment_id.hr_contract_id', store=True)
    approved_date = fields.Date('Amendment Approved on')
    effective_date = fields.Date(related='amendment_id.effective_date', store=True)

    from_date = fields.Date(string='From')
    to_date = fields.Date(string='To')

    @api.depends('contract_elem_conf_id', 'change_value', 'current_package')
    def _compute_new_package(self):
        for rec in self:
            rec.new_package = rec.current_package + rec.change_value

    @api.onchange('contract_elem_conf_id', 'amendment_id')
    def onchange_name(self):
        for package in self:
            contract = package.amendment_id.hr_contract_id
            if not contract:
                raise ValidationError(_('Please select Contract first.'))
            elif contract:
                contract_element_line_ids = contract.contract_element_line_ids
                current_package = 0
                current_from_date = False
                current_to_date = False
                for line in contract_element_line_ids:
                    if package.contract_elem_conf_id.id == line.contract_elem_conf_id.id:
                        current_package = line.amount
                        current_from_date = line.from_date
                        current_to_date = line.to_date
                package.current_package = current_package
                package.from_date = current_from_date
                package.to_date = current_to_date

