from odoo import models, fields, api


class Account(models.Model):
    _inherit = 'account.account'


    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        if self._context.get('complete_search'):
            if name and name.isdigit():
                args += [('code', '=', name)]
        return super().name_search(name, args, operator, limit)
