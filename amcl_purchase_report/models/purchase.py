# -*- coding: utf-8 -*-
import json
from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def get_total_with_tax(self):
        total_json = json.loads(self.tax_totals_json)
        total_json.update({
            'currency_symbol':self.currency_id.symbol
            })
        return total_json

    def get_tax_amount(self):
        total_json = json.loads(self.tax_totals_json)
        if total_json.get('groups_by_subtotal'):
            total_tax_amount = total_json.get('groups_by_subtotal').get(
            'Untaxed Amount')[0].get('tax_group_amount')
        else:
            total_tax_amount = 0
        return total_tax_amount

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
