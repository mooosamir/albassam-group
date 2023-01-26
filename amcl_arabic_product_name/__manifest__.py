# -*- encoding: utf-8 -*-
{
    'name': "Arabic Product Name",
    'version': '15.0.1.0.1',
    'summary': 'Arabic Product Name',
    'category': 'Other',
    'description': """Arabic Product Name""",
    "depends" : ['base', 'product', 'account', 'l10n_gcc_invoice'],
    'data': [
            'views/product_view.xml',
            'report/invoice_report_template.xml',
             ],
    "images": [],
    'license': 'LGPL-3',

    'installable' : True,
    'application' : True,
    'auto_install' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
