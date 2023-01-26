# -*- coding: utf-8 -*-
{
    'name': 'AMCL : Amendments with config',
    'category': 'Sales',
    'sequence': 1,
    'version': '15.0.1.0.1',
    'license': 'LGPL-3',
    'summary': """AMCL Access Rights""",
    'description': """AMCL Access Rights""",
    'author': 'AMCL',
    'depends': ['base', 'amcl_hr_contract_config', 'amcl_hr_contract_amendment'],
    'data': [
        'security/ir.model.access.csv',
        'views/contract_amendment_view.xml',
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
