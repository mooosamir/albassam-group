# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    'name': 'AMCL: Payslip Pivot View',
    'summary': """Payslip Pivot""",
    'description': """
        Payslip Pivot
    """,
    'version': '15.0.1.0.1',
    'author': 'AMCL',
    'depends': ['base', 'hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_payroll_custom_report_view.xml',
        'wizard/payroll_report_wizard_view.xml',
    ],
    "price": 0.0,
    "currency": "EUR",
    'installable': True,
    'application': True,
    'auto_install': False,
}
