# -*- coding: utf-8 -*-
{
    'name': 'AMCL: Purchase Comparision PDF',
    'category': 'Purchases',
    'sequence': 1,
    'version': '15.0.1',
    'license': 'LGPL-3',
    'summary': """AMCL: Purchase Comparision PDF""",
    'description': """AMCL: Purchase Comparision PDF""",
    'depends': ['base','purchase', 'purchase_requisition'],
    'data': [
        'views/purchase_requisition_view.xml',
        'report/purchase_comparision.xml',
        'report/purchase_comparision_template.xml',
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
