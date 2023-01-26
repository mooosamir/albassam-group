from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import AccessError, UserError, ValidationError
from itertools import groupby


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.depends('order_line.price_total')
    def _amount_discount(self):
        """
        Compute the total discount of PO.
        """
        for order in self:
            amount_discount = 0.0
            for line in order.order_line:
                amount_discount += (line.product_qty * line.price_unit * line.discount) / 100
            order.update({
                'amount_discount': order.currency_id.round(amount_discount),
            })

    discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')], string='Discount type',
                                     readonly=True,
                                     states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                     default='amount')
    discount_rate = fields.Monetary('Discount Rate', digits=dp.get_precision('Account'),
                                 readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_amount_discount',
                                      digits=dp.get_precision('Account'), tracking=True)

    def action_create_invoice(self):
        """Create the invoice associated to the PO.
        """
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        # 1) Prepare invoice vals and clean-up the section lines
        invoice_vals_list = []
        sequence = 10
        for order in self:
            if order.invoice_status != 'to invoice':
                continue

            order = order.with_company(order.company_id)
            pending_section = None
            # Invoice values.
            invoice_vals = order._prepare_invoice()
            # Invoice line values (keep only necessary sections).
            for line in order.order_line:
                if line.display_type == 'line_section':
                    pending_section = line
                    continue
                if not float_is_zero(line.qty_to_invoice, precision_digits=precision):
                    if pending_section:
                        line_vals = pending_section._prepare_account_move_line()
                        line_vals.update({'sequence': sequence})
                        invoice_vals['invoice_line_ids'].append((0, 0, line_vals))
                        sequence += 1
                        pending_section = None
                    line_vals = line._prepare_account_move_line()
                    line_vals.update({'sequence': sequence})
                    invoice_vals['invoice_line_ids'].append((0, 0, line_vals))
                    sequence += 1
            invoice_vals_list.append(invoice_vals)

        if not invoice_vals_list:
            raise UserError(_('There is no invoiceable line. If a product has a control policy based on received quantity, please make sure that a quantity has been received.'))

        # 2) group by (company_id, partner_id, currency_id) for batch creation
        new_invoice_vals_list = []
        for grouping_keys, invoices in groupby(invoice_vals_list, key=lambda x: (x.get('company_id'), x.get('partner_id'), x.get('currency_id'))):
            origins = set()
            payment_refs = set()
            refs = set()
            ref_invoice_vals = None
            for invoice_vals in invoices:
                if not ref_invoice_vals:
                    ref_invoice_vals = invoice_vals
                else:
                    ref_invoice_vals['invoice_line_ids'] += invoice_vals['invoice_line_ids']
                origins.add(invoice_vals['invoice_origin'])
                payment_refs.add(invoice_vals['payment_reference'])
                refs.add(invoice_vals['ref'])
            ref_invoice_vals.update({
                'ref': ', '.join(refs)[:2000],
                'invoice_origin': ', '.join(origins),
                'payment_reference': len(payment_refs) == 1 and payment_refs.pop() or False,
            })
            new_invoice_vals_list.append(ref_invoice_vals)
        invoice_vals_list = new_invoice_vals_list

        # 3) Create invoices.
        moves = self.env['account.move']
        AccountMove = self.env['account.move'].with_context(default_move_type='in_invoice')
        for vals in invoice_vals_list:
            moves |= AccountMove.with_company(vals['company_id']).create(vals)

        # 4) Some moves might actually be refunds: convert them if the total amount is negative
        # We do this after the moves have been created since we need taxes, etc. to know if the total
        # is actually negative or not
        print(moves.discount_rate)
        moves.filtered(lambda m: m.currency_id.round(m.amount_total) < 0).action_switch_invoice_into_refund_credit_note()
        moves.supply_rate()

        return self.action_view_invoice(moves)

    def action_view_invoice(self, invoices=False):
        result = super(PurchaseOrder, self).action_view_invoice()
        new_context = result['context'].split('}')
        result['context'] = new_context[0] + f", 'default_discount_type': '{self.discount_type}', 'default_discount_rate': {self.discount_rate}" + "}"
        return result

    def _prepare_invoice(self):
        vals = super(PurchaseOrder, self)._prepare_invoice()
        vals['discount_type'] = self.discount_type
        vals['discount_rate'] = self.discount_rate
        return vals

    @api.onchange('discount_type', 'discount_rate', 'order_line')
    def supply_rate(self):
        if self.discount_rate:
            for order in self:
                if order.discount_type == 'percent':
                    for line in order.order_line:
                        line.discount = order.discount_rate
                else:
                    total = discount = 0.0
                    for line in order.order_line:
                        total += round((line.product_qty * line.price_unit))
                    if order.discount_rate != 0:
                        discount = (order.discount_rate / total) * 100
                    else:
                        discount = order.discount_rate
                    for line in order.order_line:
                        line.discount = discount
                        line.discount_value = line.price_unit * line.product_qty * (discount / 100)


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    discount_value = fields.Float('Discount Value',)
    discount = fields.Float(string='Discount (%)',)
    # price_subtotal = fields.Monetary(compute='_compute_amount1', string='Subtotal', store=True)
    # price_total = fields.Monetary(compute='_compute_amount1', string='Total', store=True)
    # price_tax = fields.Monetary(compute='_compute_amount1', string='Tax', store=True)

    # @api.onchange('price_unit')
    # def onchange_discount(self):
    #     if self.price_unit:
    #         print "hutuuu"
    #         self.discount_value = self.price_unit * self.product_qty * (self.discount / 100)
    #         self.discount = (self.discount_value / (self.price_unit * self.product_qty)) * 100

    @api.depends('product_qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.taxes_id.compute_all(price, line.order_id.currency_id, line.product_qty,
                                              product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    @api.onchange('discount_value')
    def onchange_discount_value(self):
        if self.discount_value and self.price_unit and self.product_qty:
            self.discount = (self.discount_value / (self.price_unit * self.product_qty)) * 100
        else:
            self.discount = 0

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'discount')
    def _compute_amount1(self):
        # super(PurchaseOrderLine, self)._compute_amount()
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.taxes_id.compute_all(price, line.order_id.currency_id, line.product_qty,
                                              product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


    _sql_constraints = [
        ('discount_limit', 'CHECK (discount <= 100.0)',
         'Discount must be lower than 100%.'),
    ]

    def _get_discounted_price_unit(self):
        """Inheritable method for getting the unit price after applying
        discount(s).

        :rtype: float
        :return: Unit price after discount(s).
        """
        self.ensure_one()
        if self.discount:
            return self.price_unit * (1 - self.discount / 100)
        return self.price_unit

    def _get_stock_move_price_unit(self):
        """Get correct price with discount replacing current price_unit
        value before calling super and restoring it later for assuring
        maximum inheritability. We have to also switch temporarily the order
        state for avoiding an infinite recursion.
        """
        price_unit = False
        price = self._get_discounted_price_unit()
        if price != self.price_unit:
            # Only change value if it's different
            self.order_id.state = 'draft'
            price_unit = self.price_unit
            self.price_unit = price
        price = super(PurchaseOrderLine, self)._get_stock_move_price_unit()
        if price_unit:
            self.price_unit = price_unit
            self.order_id.state = 'purchase'
        return price
