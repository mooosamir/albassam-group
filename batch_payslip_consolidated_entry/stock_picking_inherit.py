# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    hide_quantity = fields.Boolean('Hide Quantity', compute='_compute_hide_quantity')

    @api.depends('check_ids')
    def _compute_hide_quantity(self):
        self.hide_quantity = False
        if self.check_ids:
            self.hide_quantity = True

