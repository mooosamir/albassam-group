# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = "account.payment"

    alternate_account_id = fields.Many2one('account.account', string="Alternate Accounts")
    allow_alternate_accounts = fields.Boolean(related='journal_id.allow_alternate_accounts', string='Allow Alternative Accounts')

    @api.depends('journal_id', 'payment_type', 'payment_method_line_id', 'alternate_account_id')
    def _compute_outstanding_account_id(self):
        for pay in self:
            if pay.alternate_account_id:
                if pay.payment_type == 'inbound':
                    pay.outstanding_account_id = pay.alternate_account_id
                elif pay.payment_type == 'outbound':
                    pay.outstanding_account_id = pay.alternate_account_id
                else:
                    pay.outstanding_account_id = False
            else:
                if pay.payment_type == 'inbound':
                    pay.outstanding_account_id = (pay.payment_method_line_id.payment_account_id
                                                  or pay.journal_id.company_id.account_journal_payment_debit_account_id)
                elif pay.payment_type == 'outbound':
                    pay.outstanding_account_id = (pay.payment_method_line_id.payment_account_id
                                                  or pay.journal_id.company_id.account_journal_payment_credit_account_id)
                else:
                    pay.outstanding_account_id = False

    def _get_valid_liquidity_accounts(self):
        res = super()._get_valid_liquidity_accounts()
        if self.alternate_account_id:
            res += (
                self.alternate_account_id,
                )
        return res

    def write(self, vals):
        old_outstanding_account = self.outstanding_account_id
        res = super().write(vals)
        if 'alternate_account_id' in vals:
            self.update_move_lines(old_outstanding_account)
        return res

    def update_move_lines(self, old_outstanding_account):
        if self.move_id.state == 'draft':
            for line in self.move_id.line_ids:
                if line.account_id.id == old_outstanding_account.id:
                    line.write({
                        'account_id': self.outstanding_account_id.id
                        })


