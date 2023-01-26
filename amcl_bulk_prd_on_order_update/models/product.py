# -*- coding: utf-8 -*-
from odoo import models, fields, _
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = 'product.template'


    def change_product_on_order(self):
        self.validate_prd_for_create_on_order()
        view_id = self.env.ref('amcl_bulk_prd_on_order_update.update_product_create_on_order_view_form')
        return {
            'name': 'Update Product Create On Order',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'amcl.prd.create.on.order.update',
            'view_id': view_id.id,
            'target': 'new',
            'context': {
                'default_product_ids': [(4, each.id) for each in self]
            }
        }

    def validate_prd_for_create_on_order(self):
        for prd in self:
            if prd.detailed_type != 'service':
                raise ValidationError(_("Please Select only 'Service' type products."))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: