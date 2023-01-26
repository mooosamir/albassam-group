# -*- encoding: utf-8 -*-

from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'

    is_customer = fields.Boolean(string='Is a Customer')
    old_customer_rank = fields.Integer(string='Old Customer Rank', default=0)
    is_supplier = fields.Boolean(string='Is a Vendor')
    old_supplier_rank = fields.Integer(string='Old Vendor Rank', default=0)

    @api.onchange('is_customer')
    def onchange_customer(self):
        for each in self:
            if each.is_customer:
                each.customer_rank = 1 if each.old_customer_rank == 0 else each.old_customer_rank
            else:
                each.old_customer_rank = each.customer_rank
                each.customer_rank = 0

    @api.onchange('is_supplier')
    def onchange_supplier(self):
        for each in self:
            if each.is_supplier:
                each.supplier_rank = 1 if each.old_supplier_rank == 0 else each.old_supplier_rank
            else:
                each.old_supplier_rank = each.supplier_rank
                each.supplier_rank = 0
