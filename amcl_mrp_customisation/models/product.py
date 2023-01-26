# -*- coding: utf-8 -*-

from odoo import fields, models , api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    can_be_processed = fields.Boolean('Can Be Processed')
    is_input = fields.Boolean(string='Is Input')
    is_output = fields.Boolean(string='Is Output')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        if self._context.get('not_show_can_be_processed'):
            args += [('can_be_processed', '=', False)]
        if self._context.get('show_inputs'):
            args += [('is_input', '=', True)]
        if self._context.get('show_outputs'):
            args += [('is_output', '=', True)]
        res = super().name_search(name, args, operator, limit)
        return res
