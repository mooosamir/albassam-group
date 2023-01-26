# -*- coding: utf-8 -*-

from . import models

from odoo import api, SUPERUSER_ID

def update_customers(env):
    partner_ids = env['res.partner'].search([('customer_rank','>',0)])
    partner_ids.write({
        'is_customer': True
        })

def update_vendors(env):
    supplier_ids = env['res.partner'].search([('supplier_rank','>',0)])
    supplier_ids.write({
        'is_supplier': True
        })

def _update_fields_from_existing(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    update_customers(env)
    update_vendors(env)
