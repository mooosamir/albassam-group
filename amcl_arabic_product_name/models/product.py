# -*- encoding: utf-8 -*-
from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'product.template'

    arabic_name = fields.Char(string='Arabic Product Name')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
