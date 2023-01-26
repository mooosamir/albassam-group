# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AddMultiTransfer(models.TransientModel):
    _name = 'stock.internal.transfer.add_multiple'
    _description = 'Internal Transfer add multiple'

    quantity = fields.Float('Quantity',
                            default=1.0)
    products_ids = fields.Many2many(
        'product.product',
        string='Products',
        domain=[('sale_ok', '=', True)],
    )

    
    def add_multiple(self):
        active_id = self._context['active_id']
        list_of_vals = []
        for product_id in self.products_ids:
            val = {
                'product_qty': self.quantity,
                'transfer_id': active_id,
                'product_id': product_id.id or False,
                'product_uom': product_id.uom_po_id.id,
            }
            list_of_vals.append(val)
        self.env['stock.transfer.internal'].browse(active_id).write(
            {'lines': [(0, 0, line) for line in list_of_vals]})


AddMultiTransfer()
