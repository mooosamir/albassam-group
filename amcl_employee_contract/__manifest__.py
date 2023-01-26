# -*- coding: utf-8 -*-
{
    'name': 'AMCL:Employee Contracts',
    'category': 'contracts',
    'sequence': 1,
    'version': '15.0.1',
    'license': 'LGPL-3',
    'summary': """Employee Contracts""",
    'description': """Employee Contracts""",
    'depends': [
                'base',
                'hr',
                'hr_payroll',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_contract_elements_view.xml',
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
