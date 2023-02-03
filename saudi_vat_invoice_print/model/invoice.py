# -*- coding: utf-8 -*-

import binascii

from num2words import num2words
from odoo import api, models, fields
from datetime import datetime
from . import qr_code_base
import pytz
import base64

class AccountInvoiceLine(models.Model):
    _inherit = 'account.move.line'

    tax_amount = fields.Monetary('Tax amount', compute='_compute_price', store=True)
    vat_text = fields.Char('Vat Text', compute='_get_vat_text', store=True)
    discount_amount = fields.Float('Discount Amount', compute='_compute_price', store=True)
    quantity = fields.Float(string='Quantity', digits=(16, 3),
        default=1.0,
        help="The optional quantity expressed by this line, eg: number of product sold. "
             "The quantity is not a legal requirement but is very useful for some reports.")
    price_before_discount = fields.Monetary('Price B/f Disc', compute='_compute_price', store=True)
    amount_total = fields.Monetary('Price Total', compute='_compute_price')

    @api.depends('tax_ids', 'price_unit', 'quantity')
    def _get_vat_text(self):
        vat = ''
        for line in self:
            for tax in line.tax_ids:
                vat += str(tax.amount) + '%,'
            line.vat_text = vat[:-1]

    
    @api.depends('price_unit', 'discount', 'tax_ids', 'quantity',
                 'product_id', 'move_id.partner_id', 'move_id.currency_id', 'move_id.company_id',
                 'move_id.invoice_date', 'move_id.date')
    def _compute_price(self):
        for line in self:
            currency = line.move_id and line.move_id.currency_id or None
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = False
            if line.tax_ids:
                taxes = line.tax_ids.compute_all(price, currency, line.quantity, product=line.product_id,
                                                              partner=line.move_id.partner_id)
            # price_subtotal_signed = taxes['total_excluded'] if taxes else line.quantity * price
            line.update({
                'price_subtotal': taxes['total_excluded'] if taxes else line.quantity * price
            })
            # if line.move_id.currency_id and line.move_id.company_id and line.move_id.currency_id != line.move_id.company_id.currency_id:
                # price_subtotal_signed = line.move_id.currency_id.with_context(
                #     date=line.move_id._get_currency_rate_date()).compute(price_subtotal_signed,
                #                                                             line.move_id.company_id.currency_id)
            # sign = line.move_id.move_type in ['in_refund', 'out_refund'] and -1 or 1
            # line.update({
            #     'price_subtotal_signed': price_subtotal_signed * sign
            # })
            if taxes:
                line.update({
                    'tax_amount': taxes['total_included'] - taxes['total_excluded'],
                    'amount_total': taxes['total_included']
                })
            line.update({
                'price_before_discount': line.quantity * line.price_unit,
                'discount_amount': (line.price_before_discount * line.discount) / 100.0
            })

    # @api.depends('price_unit','quantity','price_subtotal')
    # def _compute_tax_amount(self):
    #     for line in self:
    #         line.tax_amount = line.amount_total - line.price_subtotal


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    TAG_SELLER = 1
    TAG_VAT_NO = 2
    TAG_TIME_STAMP = 3
    TAG_TOTAL = 4
    TAG_VAT_TOTAL = 5

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        res.update({
            'approved_by': self.env.user.partner_id.id
            })
        return res

    @api.model
    def create(self, vals):
        if vals.get('partner_id',False):
            vals.update({
                'attention': vals.get('partner_id')
                })
        return super().create(vals)

    @api.onchange('partner_id')
    def onchange_partner(self):
        if self.partner_id:
            self.attention = self.partner_id.id

    invoice_date_time = fields.Datetime('Invoice Date Time')
    amount_text = fields.Char(string='Amount In Words', compute='amount_to_words')
    amount_in_ar = fields.Char(string='Amount In Words', compute='amount_to_words')
    attention = fields.Many2one('res.partner', 'Attention')
    approved_by = fields.Many2one('res.partner', 'Approved By')
    vat_text = fields.Char('Vat Text', compute='_get_vat_text')
    vat_arabic_text = fields.Char('Vat Text(Arabic)', compute='_get_vat_text')
    discount = fields.Float('Discount', compute='compute_all_price')
    price_before_discount = fields.Monetary('Total ( Excluded VAT)', compute='compute_all_price')
    # qr_image = fields.Binary("QR Code", compute='_generate_qr_code')
    # qr_data = fields.Char("QR Data", compute='_generate_qr_code')
    delivery_date = fields.Date('Delivery Date')
    bank_id = fields.Many2one('res.bank', 'Receiving Bank')
    receipt_number = fields.Char('Receipt Number')
    contract_no = fields.Char('Contract No')
    job_number = fields.Char('Job Number')
    sale_order_id = fields.Many2one('sale.order', compute='_compute_sale_order_id')

    
    @api.depends('company_id', 'invoice_date_time', 'amount_tax', 'amount_total')
    def _generate_qr_code(self):
        for invoice in self:
            data = "Seller : {} \n" \
                   "Seller VAT No. : {} \n" \
                   "Invoice Date Time : {} \n" \
                   "Total Vat Amount : {} \n" \
                   "Total Invoice Amount : {}".format(invoice.company_id.name, invoice.company_id.vat,
                                                      invoice.invoice_date_time,
                                                      invoice.amount_tax, invoice.amount_total)
            invoice.update({
                'qr_data': data,
                # 'qr_image' : qr_code_base.generate_qr_code(data)
            })


    def _data_hex(self, value, tag):

        hex_tag = self._convert_int_to_hex(tag)
        hex_len = self._convert_int_to_hex(len(value.encode("UTF-8")))
        hex_val = self._convert_str_to_hex(value)
        return "%s%s%s" % (hex_tag, hex_len, hex_val)

    def _seller_hex(self, value):
        return self._data_hex(value, self.TAG_SELLER)

    def _vat_no_hex(self, value):
        return self._data_hex(value, self.TAG_VAT_NO)

    def _time_stamp_hex(self, value):
        return self._data_hex(value, self.TAG_TIME_STAMP)

    def _total_hex(self, value):
        return self._data_hex(value, self.TAG_TOTAL)

    def _vat_total_hex(self, value):
        return self._data_hex(value, self.TAG_VAT_TOTAL)

    def _convert_int_to_hex(self, value):
        return "%0.2x" % value

    def _convert_str_to_hex(self, value):
        hex_val = ""
        if value:
            str_bytes = value.encode("UTF-8")
            encoded_hex = binascii.hexlify(str_bytes)
            hex_val = encoded_hex.decode("UTF-8")

        return hex_val

    def _convert_text_to_base64(self, value):
        # value_bytes = value.decode('utf-8')
        base64_bytes = base64.b64encode(value)
        return base64_bytes.decode("utf-8")

    def generate_tlv_code(self):
        self.invalidate_cache()
        DEFAULTE_TZ = 'Asia/Riyadh'
        hex_seller = False
        hex_vat_no = False
        hex_time_stamp = False
        total = False
        vat_total = False
        # time_stamp = datetime.now(
        #     pytz.timezone(self.env.user.tz or self._context.get('tz', DEFAULTE_TZ))).strftime('%Y-%m-%dT%H:%M:%SZ')

        localFormat = "%Y-%m-%d %H:%M:%S"

        # Convert date to current user timezone or Saudi Arabia in default case.
        create_date = self.create_date.strftime('%Y-%m-%d %H:%M:%S')
        utcmoment_naive = datetime.strptime(create_date, localFormat)
        utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)

        tz_ = self.env.user.tz or self._context.get('tz', DEFAULTE_TZ)
        localDatetime = utcmoment.astimezone(pytz.timezone(tz_))

        time_stamp = localDatetime.strftime('%Y-%m-%dT%H:%M:%SZ')
        hex_seller = self._seller_hex(self.company_id.name or "")
        hex_vat_no = self._vat_no_hex(self.company_id.vat or "")
        hex_time_stamp = self._time_stamp_hex(time_stamp)
        hex_total = self._total_hex(str(self.amount_total))
        hex_vat_total = self._vat_total_hex(str(self.amount_tax))

        hex_text = "%s%s%s%s%s" % (hex_seller, hex_vat_no, hex_time_stamp, hex_total, hex_vat_total)
        code_qr = self._convert_text_to_base64(bytearray.fromhex(hex_text))

        return code_qr


    
    def _compute_sale_order_id(self):
        if not self.sale_order_id:
            sale_line_ids = self.invoice_line_ids.mapped('sale_line_ids')
            if sale_line_ids:
                self.sale_order_id = sale_line_ids[0].order_id.id
            else:
                sale = self.env['sale.order'].search([('name', '=', self.invoice_origin)], limit=1)
                self.sale_order_id = sale.id

    @api.depends('invoice_line_ids.quantity', 'invoice_line_ids.price_unit', 'amount_untaxed', 'amount_tax')
    def compute_all_price(self):
        for invoice in self:
            price_before_discount = discount = 0
            for line in invoice.invoice_line_ids:
                price_before_discount += line.quantity * line.price_unit
                discount += line.discount * (line.quantity * line.price_unit) / 100
                print(line.discount_amount)
            invoice.update({
                'price_before_discount': price_before_discount,
                'discount': discount
            })

    @api.depends('invoice_line_ids', 'amount_total')
    def _get_vat_text(self):
        vat = ''
        arab = ''
        for tax in self.mapped('invoice_line_ids.tax_ids'):
            vat += str(tax.amount) + '%,'
            arab += str(tax.amount_in_arabic) + '%,'
        self.vat_text = vat[:-1]
        self.vat_arabic_text = arab[:-1]

    def amount_to_words(self):
        for invoice in self:
            amount_in_eng = num2words(invoice.amount_total, to='currency',
                                      lang='en')

            amount_in_eng = amount_in_eng.replace('euro', 'riyals')
            amount_in_eng = amount_in_eng.replace('cents', 'halala')
            invoice.update({
                'amount_text':amount_in_eng,
                'amount_in_ar':num2words(invoice.amount_total, to='currency',
                                          lang='ar')
            })

    def invoice_print(self):
        self.ensure_one()
        self.sent = True
        return self.env['report'].get_action(self, 'custom_azmi_holding.report_azmi_invoicerishi_format_pdt')

    # 
    # def action_invoice_proforma2(self):
    #     invoice = super(AccountInvoice, self).action_invoice_proforma2()
    #     if self.type in ('out_invoice', 'in_refund'):
    #         number = self.journal_id.sequence_id.with_context(ir_sequence_date=self.date).next_by_id()
    #         self.number = number
    #         self.move_name = number
    #     return invoice

    # @api.model
    # def create(self, vals):
    #     invoice = super(AccountInvoice, self).create(vals)
    #     if invoice.move_type in ('out_invoice', 'in_refund'):
    #         number = invoice.journal_id.sequence_id.with_context(ir_sequence_date=invoice.date).next_by_id()
    #         invoice.name = number
    #         invoice.move_name = number
    #     return invoice


class AccountTax(models.Model):
    _inherit = 'account.tax'

    amount_in_arabic = fields.Float('Amount in Arabic')

