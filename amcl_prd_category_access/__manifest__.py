# -*- coding: utf-8 -*-
{
    'name': 'AMCL : Product Category Access',
    'category': 'Sales',
    'sequence': 1,
    'version': '15.0.1.0.2',
    'license': 'LGPL-3',
    'summary': """Multi company product category access right""",
    'description': """Multi company product category access right""",
    'author': 'AMCL',
    'depends': ['base', 'product'],
    'data': [
        'security/security.xml',
        'views/product_category_view.xml',
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
