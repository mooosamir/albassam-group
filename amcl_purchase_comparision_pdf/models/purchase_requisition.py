from odoo import fields, models


class PurchaseRequisition(models.AbstractModel):
    _inherit = 'purchase.requisition'


    def action_print_pdf_report(self):
        report_id = self.env.ref('amcl_purchase_comparision_pdf.product_comparision_report')
        return report_id.report_action(self)

    def get_purchase_comparison_lines(self):
        values = []
        values = self.env['purchase.order'].search_read([('requisition_id','=',self.id)], ['partner_id','amount_total'])
        return values
