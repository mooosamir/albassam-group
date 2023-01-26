# -*- coding: utf-8 -*-
{
    'name': 'AMCL : Import Data',
    'category': 'Sales',
    'sequence': 1,
    'version': '15.0.1',
    'license': 'LGPL-3',
    'summary': """AMCL : Import Data""",
    'description': """AMCL : Import Data""",
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_data_wizard_view.xml',
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
