# -*- coding: utf-8 -*-
{
    'name': 'AMCL : Update Product Policy',
    'category': 'Product',
    'sequence': 1,
    'version': '15.0.1',
    'license': 'LGPL-3',
    'summary': """AMCL : Update Product Policy""",
    'description': """AMCL : Update Product Policy""",
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
