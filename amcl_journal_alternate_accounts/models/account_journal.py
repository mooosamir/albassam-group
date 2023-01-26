# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = "account.journal"


    allow_alternate_accounts = fields.Boolean(string="Allow Alternative Accounts")
    alternative_account_ids = fields.Many2many("account.account",
                                            "journal_id", 
                                            'account_id',
                                            string="Alternative Account",
                                            domain="[('deprecated', '=', False), ('company_id', '=', company_id),"
               "'|', ('user_type_id', '=', default_account_type), ('user_type_id', 'in', type_control_ids),"
               "('user_type_id.type', 'not in', ('receivable', 'payable'))]")
