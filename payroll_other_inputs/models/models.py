# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OtherInputs(models.Model):
    _name = 'other.inputs'
    _description = 'Other Inputs'

    name = fields.Char('Description')
    other_employee_id = fields.Many2one('hr.employee', string='Employee', )
    other_date = fields.Date('Date')
    other_amount = fields.Float('Amount')
    other_input_type_id = fields.Many2one('hr.payslip.input.type', string='Type', required=True)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')
    
    def action_confirm(self):
        self.write({'state': 'done'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

class HrPayslipInherit(models.Model):
    _inherit = 'hr.payslip'

    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee_other_input(self):
        other_input_employee = self.env['other.inputs'].search([
            ('other_employee_id', '=', self.employee_id.id),
            ('other_date', '>=', self.date_from), ('other_date', '<=', self.date_to)])

        if other_input_employee:
            lines = []
            self.input_line_ids = False
            for rec in other_input_employee:
                vals = {
                    'input_type_id': rec.other_input_type_id.id,
                    'name': rec.name,
                    'amount': rec.other_amount,
                }
                lines.append((0, 0, vals))
            self.input_line_ids = lines
