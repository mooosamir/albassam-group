# -*- coding: utf-8 -*-
{
    'name': 'AMCL: Multi Vendor Agreement',
    'category': 'Purchase',
    'sequence': 1,
    'version': '15.0.1.0.1',
    'license': 'LGPL-3',
    'summary': """Multiple Vendor in Purchase Agreement""",
    'description': """Multiple Vendor in Purchase Agreement""",
    'author': 'AMCL',
    'depends': ['base', 'purchase_requisition'],
    'data': [
        'views/purchase_requisition_view.xml',
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
