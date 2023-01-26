# -*- encoding: utf-8 -*-
from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'hr.employee'

    middle_name = fields.Char(size=64, string='Middle Name')
    grand_father_name = fields.Char(size=64, string='Grand Father Name')
    last_name = fields.Char(size=64, string='Last Name')
    full_name = fields.Char(string='Full Name', compute='_get_full_name')

    @api.depends('name', 'middle_name', 'grand_father_name', 'last_name')
    def _get_full_name(self):
        for rec in self:
            if rec.name and rec.middle_name and rec.grand_father_name and rec.last_name:
                rec.full_name = "%s %s %s %s" % (rec.name or '', rec.middle_name or '', rec.grand_father_name or '', rec.last_name or '')
            else:
                rec.full_name = "%s %s %s" % (rec.name or '', rec.middle_name or '', rec.last_name or '')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
