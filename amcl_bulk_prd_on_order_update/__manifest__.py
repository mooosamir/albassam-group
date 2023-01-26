# -*- coding: utf-8 -*-
{
    'name': 'AMCL : Update Product Create On Option',
    'category': 'Product',
    'sequence': 1,
    'version': '15.0.1',
    'license': 'LGPL-3',
    'summary': """AMCL : Create On Option""",
    'description': """AMCL : Create On Option""",
    'depends': ['base', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'wizard/product_wizard_view.xml',
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
