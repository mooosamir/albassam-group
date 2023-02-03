from odoo import api, models, fields, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_is_zero, float_compare, pycompat


class AccountMove(models.Model):
    _inherit = 'account.move'

    amount_retention = fields.Monetary(string='Retention', store=True,
                                       readonly=True, compute='_get_retention_amount')
    retention_id = fields.Many2one('sale.retention', string='Retention')

    @api.depends('retention_id', 'amount_untaxed', 'amount_total')
    def _get_retention_amount(self):
        for record in self:
            if record.retention_id.retention_type == 'tax_excl':
                record.amount_retention  = (record.retention_id.retention_percent / 100) * record.amount_untaxed
            else:
                record.amount_retention = (record.retention_id.retention_percent / 100) * record.amount_total
            record.update_amount_retention_in_lines()

    @api.model
    def prepare_retention_line(self, vals):
        retention_id = self.env['sale.retention'].browse(vals.get('retention_id'))
        amount_retention = vals.get('amount_retention')
        line_values = {
            'display_type': False,
            'sequence': 0,
            'name': retention_id.name,
            'quantity': 1.0,
            'price_unit': -amount_retention,
            'exclude_from_invoice_tab': True,
            'account_id': retention_id.retention_account.id,
            'journal_id': vals.get('journal_id'),
            'debit': amount_retention,
            'retention_line': True,
        }
        return line_values

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            retention_line_vals = False
            if 'retention_id' in vals and vals.get('retention_id', False) and vals.get('move_type') == 'out_invoice':
                retention_line_vals = self.prepare_retention_line(vals)
                vals['invoice_line_ids'].append((0, 0, retention_line_vals))
        res = super().create(vals_list)
        return res

    def update_amount_retention_in_lines(self):
        retention_line = self.line_ids.filtered(lambda line: line.retention_line)
        # debit_line = self.get_debit_line()
        # debit_amount = debit_line.price_unit - self.amount_retention
        if retention_line:
            if self.amount_retention:
                self.write({
                    'line_ids': [(1,retention_line.id,{
                        'price_unit': -self.amount_retention,
                        'debit': self.amount_retention,
                        'account_id': self.retention_id and self.retention_id.retention_account.id,
                        'name': self.retention_id.name,
                        })]
                    })
            else:
                self.write({
                    'line_ids': [(2,retention_line.id)]
                    })
        else:
            if self.amount_retention:
                line_vals = self.prepare_retention_line({
                    'journal_id': self.journal_id.id,
                    'amount_retention': self.amount_retention,
                    'retention_id': self.retention_id.id
                    })
                self.write({
                    'line_ids': [(0,0,line_vals)]
                    })
        self._recompute_dynamic_lines()


    def get_debit_line(self):
        for line in self.line_ids:
            if not line.retention_line and line.debit>0:
                return line
        return False


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    retention_line = fields.Boolean(string='Retention')
