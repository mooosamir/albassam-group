# -*- coding: utf-8 -*-
{
    'name': 'Saudi Invoice Format',
    'version': '1.0',
    'depends': ['base','account','sale'],
    'category': 'Accounting',
    'data': [
        'views/res_company.xml',
        'views/invoice.xml',
        'views/res_partner.xml',
        'views/sale.xml',
        'reports/report_saudi_invoice.xml',
        'reports/report_saudi_pro-forma_invoice.xml',
     ],
    'assets': {
        'web.report_assets_common': [
            '/saudi_vat_invoice_print/static/src/scss/reports.scss',
        ],
    },
    'installable': True,
    'application': False,
}
