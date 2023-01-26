# -*- coding: utf-8 -*-
from odoo import fields, models

SERVICE_POLICY = [
    # (service_policy, (invoice_policy, service_type), string)
    ('ordered_timesheet', ('order', 'timesheet'), 'Prepaid/Fixed Price'),
    ('delivered_timesheet', ('delivery', 'timesheet'), 'Based on Timesheets'),
    ('delivered_manual', ('delivery', 'manual'), 'Based on Milestones'),
]
SERVICE_TO_GENERAL = {policy[0]: policy[1] for policy in SERVICE_POLICY}
GENERAL_TO_SERVICE = {policy[1]: policy[0] for policy in SERVICE_POLICY}

class UpdateProductPloicy(models.TransientModel):
   _name = 'amcl.prd.policy.update'
   _description = 'Product Type Update'


   service_policy = fields.Selection([
        (policy[0], policy[2]) for policy in SERVICE_POLICY
    ], string="Service Invoicing Policy", required=True)
   product_ids = fields.Many2many('product.template', string='Products')


   def action_to_change_policy(self):
      self.product_ids.write({
                'service_policy': self.service_policy
                })

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: