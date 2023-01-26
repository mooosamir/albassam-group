# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = "product.category"

    company_id = fields.Many2one('res.company', string='Company')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
