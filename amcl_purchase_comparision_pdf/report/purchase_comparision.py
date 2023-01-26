from odoo import fields, models, api


class PurchaseRequisitionCompare(models.AbstractModel):
    _name = 'report.amcl_purchase_comparision_pdf.purchase_requisition_compare'
    _description = 'Purchase Requisition Compare Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print ("\n 1111111111111111")
        docs = self.env['purchase.requisition'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'purchase.requisition',
            'docs':docs,
            'report_type': data.get('report_type') if data else '',
        }
