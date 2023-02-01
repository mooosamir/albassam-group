# -*- coding: utf-8 -*-
{
    'name': 'AMCL: Payslip Print',
    'category': 'Payroll',
    'sequence': 1,
    'version': '15.0.1.0.1',
    'license': 'LGPL-3',
    'summary': """Payslip Print""",
    'description': """Payslip Print""",
    'author': 'AMCL',
    'depends': ['base', 'hr_payroll'],
    'data': [
        'report/report.xml',
        'report/hr_payroll_report_template.xml',
        'views/hr_payroll_view.xml',
    ],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
