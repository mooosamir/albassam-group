from odoo import fields, models


class AccountAccount(models.Model):
	_inherit = 'account.account'

	group_id = fields.Many2one('account.group', compute='_compute_account_group', store=True, readonly=False,
                               help="Account prefixes can determine account groups.")