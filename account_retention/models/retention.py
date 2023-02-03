# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Retention(models.Model):
    _name = 'sale.retention'
    _inherit = 'mail.thread'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string="Active", default=True)
    number = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                         index=True, default=lambda self: _('New'))
    retention_type = fields.Selection([('tax_excl', 'Exclude Tax'), ('tax_incl', 'Include Tax')], default='tax_incl',
                                      track_visibility='onchange', required=True)
    retention_account = fields.Many2one('account.account', string='Account', required=True)
    retention_percent = fields.Float(string='Percent(%)')

    @api.constrains('retention_percent')
    def check_retention(self):
        for rec in self:
            if rec.retention_percent <= 0:
                raise ValidationError(_("Percent must be Non-zero +ve Number"))
            if rec.retention_percent > 100:
                raise ValidationError(_("Percent Must be less than or equal to 100"))

    @api.model
    def create(self, vals):
        if 'number' not in vals or vals['number'] == _('New'):
            vals['number'] = self.env['ir.sequence'].next_by_code('sale.retention') or _('New')
        res = super(Retention, self).create(vals)
        return res

