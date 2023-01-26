# -*- coding: utf-8 -*-

from odoo import models, api


class Account(models.Model):
    _inherit = 'account.account'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if self._context.get('filter_alternate_accounts') and self._context.get('journal_id'):
            journal_id = self.env['account.journal'].browse( self._context.get('journal_id'))
            args += [('id', 'in', journal_id.alternative_account_ids.ids)]
        res = super().name_search(name, args, operator, name_get_uid)
        return res
