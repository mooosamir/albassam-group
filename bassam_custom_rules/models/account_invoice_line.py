# -*- coding: utf-8 -*
from odoo import api, fields, models, tools


class InvoiceLine(models.Model):
    _inherit = "account.move.line"

    @api.onchange('product_id')
    def product_change(self):
        if self.product_id and self.product_id.id == 14806:  # Supply, Installation, Testing, Commissioning Of R.O plant
            if self.env.user.company_id.id == 15:  # Salah & Musaad M. Al Bassam Petroleum Equipment Company
                self.account_id = 16796  # 3101001 LC REVENUES
            if self.env.user.company_id.id == 13:  # Branch Salah & Musaad M. Al Bassam Petroleum Equipment Co.
                self.account_id = 21416  # 33 Service Revenue
            if self.env.user.company_id.id == 14:  # SAUDI WATER TECHNOLOGY LTD.
                self.account_id = 14956  # 3201001 Dammam revenue
            if self.env.user.company_id.id == 12:  # INDUSTRIAL SUPPORT SERVICES CO.
                self.account_id = 19012  # 1212 ACCRUED REVENUES
            if self.env.user.company_id.id == 11:  # Gulf Heavy Industries Company
                self.account_id = 20616  # 1205 ACCRUED REVENUES


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.model
    def _default_deposit_account_id(self):
        account_id = super(SaleAdvancePaymentInv, self)._default_deposit_account_id()
        if self._default_product_id() and self._default_product_id().id == 14806:  # Supply, Installation, Testing, Commissioning Of R.O plant
            if self.env.user.company_id.id == 15:  # Salah & Musaad M. Al Bassam Petroleum Equipment Company
                account_id = 16796  # 3101001 LC REVENUES
            if self.env.user.company_id.id == 13:  # Branch Salah & Musaad M. Al Bassam Petroleum Equipment Co.
                account_id = 21416  # 33 Service Revenue
            if self.env.user.company_id.id == 14:  # SAUDI WATER TECHNOLOGY LTD.
                account_id = 14956  # 3201001 Dammam revenue
            if self.env.user.company_id.id == 12:  # INDUSTRIAL SUPPORT SERVICES CO.
                account_id = 19012  # 1212 ACCRUED REVENUES
            if self.env.user.company_id.id == 11:  # Gulf Heavy Industries Company
                account_id = 20616  # 1205 ACCRUED REVENUES
        return account_id
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
