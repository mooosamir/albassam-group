# -*- coding: utf-8 -*-
from odoo import fields, models


class UpdateProductCreateOnOrder(models.TransientModel):
   _name = 'amcl.prd.create.on.order.update'
   _description = 'Product Create On Update'


   service_tracking = fields.Selection(
        selection=[
            ('no', 'Nothing'),
            ('task_global_project', 'Task'),
            ('task_in_project', 'Project & Task'),
            ('project_only', 'Project'),
        ],
        string="Create on Order", default="no",
        help="On Sales order confirmation, this product can generate a project and/or task. \
        From those, you can track the service you are selling.\n \
        'In sale order\'s project': Will use the sale order\'s configured project if defined or fallback to \
        creating a new project based on the selected template.", required=True)
   product_ids = fields.Many2many('product.template', string='Products')


   def action_to_change_create_on_order(self):
      self.product_ids.write({
                'service_tracking': self.service_tracking
                })

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: