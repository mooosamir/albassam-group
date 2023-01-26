# -*- coding: utf-8 -*-

import binascii

from num2words import num2words
from odoo import api, models, fields
from datetime import datetime
from . import qr_code_base
import pytz
import base64

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    TAG_SELLER = 1
    TAG_VAT_NO = 2
    TAG_TIME_STAMP = 3
    TAG_TOTAL = 4
    TAG_VAT_TOTAL = 5

    date_due = fields.Date(string='Due Date',
                           readonly=True, states={'draft': [('readonly', False)]}, index=True, copy=False)
    delivery_date = fields.Date(string='Delivery Date',
                                readonly=True, states={'draft': [('readonly', False)]}, index=True, copy=False)
    receipt_number = fields.Char(string='Receipt Number', readonly=True, states={'draft': [('readonly', False)]},
                                 index=True, copy=False)
    contract_no = fields.Char(string='Contract No', readonly=True, states={'draft': [('readonly', False)]}, index=True,
                              copy=False)
    job_number = fields.Char(string='Job Number', readonly=True, states={'draft': [('readonly', False)]}, index=True,
                              copy=False)
    # qr_data = fields.Char("QR Data", compute='_generate_qr_code')
    bank_id = fields.Many2one('res.bank', 'Receiving Bank',readonly=True, states={'draft': [('readonly', False)]},
                              copy=False)

    # 
    # @api.depends('company_id', 'date_order', 'amount_tax', 'amount_total')
    # def _generate_qr_code(self):
    #     for sale in self:
    #         data = "Seller : {} \n" \
    #                "Seller VAT No. : {} \n" \
    #                "Invoice Date Time : {} \n" \
    #                "Total Vat Amount : {} \n" \
    #                "Total Invoice Amount : {}".format(sale.company_id.name, sale.company_id.vat, sale.date_order,
    #                                                   sale.amount_tax, sale.amount_total)
    #         sale.update({'qr_data' : data })

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


    @api.onchange('invoice_payment_term_id', 'date_order')
    def _onchange_payment_term_date_order(self):
        date_order = self.date_order
        if not date_order:
            date_order = fields.Date.context_today(self)
        if not self.payment_term_id:
            # When no payment term defined
            self.date_due = self.date_due or date_order
        else:
            pterm = self.payment_term_id
            pterm_list = \
                pterm.with_context(currency_id=self.company_id.currency_id.id).compute(value=1, date_ref=date_order)
            print(pterm_list)
            self.date_due = max(line[0] for line in pterm_list)

    
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['delivery_date'] = self.delivery_date or False
        invoice_vals['receipt_number'] = self.receipt_number or False
        invoice_vals['contract_no'] = self.contract_no or False
        invoice_vals['job_number'] = self.job_number or False
        return invoice_vals
