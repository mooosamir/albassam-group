# -*- coding: utf-8 -*-
{
    'name': 'AMCL : Allow Employee',
    'category': 'Timesheet',
    'sequence': 1,
    'version': '15.0.1.0.1',
    'license': 'LGPL-3',
    'summary': """AMCL Access Rights""",
    'description': """AMCL Access Rights""",
    'author': 'AMCL',
    'depends': ['base', 'hr_timesheet', 'analytic'],
    'data': [
        'views/hr_timesheet_view.xml',
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
