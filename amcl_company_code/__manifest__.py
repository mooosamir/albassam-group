# -*- coding: utf-8 -*-
{
    'name': 'Company Code EMP Code',
    'category': 'code',
    'sequence': 1,
    'version': '15.0.1.0.2',
    'license': 'LGPL-3',
    'summary': """Company Code""",
    'description': """Company Code""",
    'depends': [
                'base',
                'hr',
                ],
    'data': [
        'data/employee_sequence.xml',
        'views/company_code_view.xml',
        'views/hr_employee_view.xml',
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
