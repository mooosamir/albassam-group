# -*- coding: utf-8 -*-
from odoo import fields, models, api, _, SUPERUSER_ID
from lxml import etree


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id, view_type, toolbar, submenu)
        advisor = self.env.user.has_group('account.group_account_manager')
        if self._context.get('default_move_type') in ['out_invoice'] or self._context.get('move_type') in ['out_invoice']:
            if view_type != 'search' and self.env.uid != SUPERUSER_ID and not advisor:
                root = etree.fromstring(res['arch'])
                root.set('create', 'false')
                res['arch'] = etree.tostring(root)
        return res

    @api.depends('restrict_mode_hash_table', 'state')
    def _compute_show_reset_to_draft_button(self):
        for move in self:
            show_reset_to_draft_button = not move.restrict_mode_hash_table and move.state in ('posted', 'cancel')
            if self._context.get('default_move_type') in ['out_invoice'] or self._context.get('move_type') in ['out_invoice']:
                if show_reset_to_draft_button and self.env.user.has_group('account.group_account_manager'):
                    show_reset_to_draft_button = True
                else:
                    show_reset_to_draft_button = False
            move.show_reset_to_draft_button = show_reset_to_draft_button

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
