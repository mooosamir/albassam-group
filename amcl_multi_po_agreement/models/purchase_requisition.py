# -*- coding: utf-8 -*-
from odoo import fields, models, api


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    vendor_ids = fields.Many2many('res.partner', 'requisition_multi_vendor_rel', string='Vendors')

    def action_create_multi_rfq(self):
        PurchaseOrder = self.env['purchase.order']
        values = PurchaseOrder.with_context(default_requisition_id=self.id,
                                    default_user_id=False).default_get(['date_order', 'company_id', 'user_id'])
        values.update({
            'requisition_id': self.id
            })
        for vendor in self.vendor_ids:
            purchase_with_vendor_id = self.env['purchase.order'].search([('requisition_id','=',self.id),
                                                ('partner_id','=', vendor.id)])
            if not purchase_with_vendor_id:
                values.update({
                    'partner_id': vendor.id,
                    'name': 'New'
                    })
                po_id = PurchaseOrder.create(values)
                self.update_po_lines(po_id)
    
    def update_po_lines(self, po_id):
        partner = po_id.partner_id
        FiscalPosition = self.env['account.fiscal.position']
        fpos = FiscalPosition.with_company(self.company_id).get_fiscal_position(partner.id)
        payment_term = partner.property_supplier_payment_term_id
        po_id.write({
            'partner_id': partner.id,
            'fiscal_position_id': fpos.id,
            'payment_term_id': payment_term.id,
            'company_id': self.company_id.id,
            'currency_id': self.currency_id.id,
            'notes': self.description,
            'date_order': fields.Datetime.now(),
            })
        if not po_id.origin or requisition.name not in po_id.origin.split(', '):
            if po_id.origin:
                if self.name:
                    po_id.origin = po_id.origin + ', ' + self.name
            else:
                po_id.origin = self.name
        if self.type_id.line_copy != 'copy':
            return
        order_lines = []
        for line in self.line_ids:
            # Compute name
            product_lang = line.product_id.with_context(
                lang=partner.lang or self.env.user.lang,
                partner_id=partner.id
            )
            name = product_lang.display_name
            if product_lang.description_purchase:
                name += '\n' + product_lang.description_purchase

            # Compute taxes
            taxes_ids = fpos.map_tax(line.product_id.supplier_taxes_id.filtered(lambda tax: tax.company_id == self.company_id)).ids

            # Compute quantity and price_unit
            if line.product_uom_id != line.product_id.uom_po_id:
                product_qty = line.product_uom_id._compute_quantity(line.product_qty, line.product_id.uom_po_id)
                price_unit = line.product_uom_id._compute_price(line.price_unit, line.product_id.uom_po_id)
            else:
                product_qty = line.product_qty
                price_unit = line.price_unit

            if self.type_id.quantity_copy != 'copy':
                product_qty = 0

            # Create PO line
            order_line_values = line._prepare_purchase_order_line(
                name=name, product_qty=product_qty, price_unit=price_unit,
                taxes_ids=taxes_ids)
            order_lines.append((0, 0, order_line_values))
        po_id.order_line = order_lines

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
