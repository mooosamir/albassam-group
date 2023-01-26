# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    @api.model
    def _set_default_require_attachment(self):
        value = False
        if self.company_id and self.company_id.name == 'INDUSTRIAL SUPPORT SERVICES CO.':
            value = True
        return value

    @api.depends('company_id')
    def set_show_require_attachment(self):
        value = False
        if self.company_id and self.company_id.name == 'INDUSTRIAL SUPPORT SERVICES CO.':
            value = True
        self.show_require_attachment = value

    show_require_attachment = fields.Boolean(string='Show Require Attachment', compute='set_show_require_attachment')
    require_attachment = fields.Boolean(string='Require Attachment', default=_set_default_require_attachment, help="If Checked then the payment term is Credit term, True when the payment term is on credit and company spceific to 'INDUSTRIAL SUPPORT SERVICES CO.'")

    @api.onchange('company_id')
    def onchange_company(self):
        value = True
        if self.company_id and self.company_id.name != 'INDUSTRIAL SUPPORT SERVICES CO.':
            value = False
        self.require_attachment = value

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
