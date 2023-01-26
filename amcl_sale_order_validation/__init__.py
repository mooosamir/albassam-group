# -*- coding: utf-8 -*-

from . import models
from odoo import api, SUPERUSER_ID

def _update_payment_term_require_attachment(env):
    iss_company_id = env['res.company'].search([('name','=','INDUSTRIAL SUPPORT SERVICES CO.')])
    if iss_company_id:
        payment_term_ids = env['account.payment.term'].search([('company_id','=',iss_company_id.id)])
        if payment_term_ids:
            payment_term_ids.write({
                'require_attachment': True
                })

def _payment_term_post_init(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _update_payment_term_require_attachment(env)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

