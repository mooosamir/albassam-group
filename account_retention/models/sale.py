# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # @api.depends('order_line.price_total')
    # def _amount_all(self):
    #     """
    #     Compute the total amounts of the SO.
    #     """
    #     for order in self:
    #         amount_untaxed = amount_tax = amount_retention = 0.0
    #         for line in order.order_line:
    #             amount_untaxed += line.price_subtotal
    #             amount_tax += line.price_tax
    #             amount_retention += line.price_retention
    #         order.update({
    #             'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
    #             'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
    #             'amount_retention': order.pricelist_id.currency_id.round(amount_retention),
    #             'amount_total': amount_untaxed + amount_tax + amount_retention,
    #         })

    @api.depends('retention_id', 'amount_untaxed', 'amount_total')
    def _get_retention_amount(self):
        for record in self:
            if record.retention_id.retention_type == 'tax_excl':
                record.amount_retention  = (record.retention_id.retention_percent / 100) * record.amount_untaxed
            else:
                record.amount_retention = (record.retention_id.retention_percent / 100) * record.amount_total

    # bank = fields.Many2one('res.partner.bank', string='Bank')
    retention_id = fields.Many2one('sale.retention', string='Retention')
    amount_retention = fields.Monetary(string='Retention', store=True,
                                       readonly=True, compute='_get_retention_amount')
    
    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        res.update({
            'retention_id': self.retention_id.id,
            'amount_retention': self.amount_retention,
            })
        return res
