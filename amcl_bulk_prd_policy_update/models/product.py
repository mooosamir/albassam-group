# -*- coding: utf-8 -*-
from odoo import models, fields, _
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = 'product.template'


    def change_product_policy(self):
        self.validate_prd_for_policy()
        view_id = self.env.ref('amcl_bulk_prd_policy_update.update_amcl_prd_policy_update_view_form')
        return {
            'name': 'Update Product Policy',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'amcl.prd.policy.update',
            'view_id': view_id.id,
            'target': 'new',
            'context': {
                'default_product_ids': [(4, each.id) for each in self]
            }
        }

    def validate_prd_for_policy(self):
        for prd in self:
            if prd.detailed_type != 'service':
                raise ValidationError(_("Please Select only 'Service' type products."))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: