# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    'name': 'AMCL: Batch Payslip Extend',
    'summary': """Batch Payslip Extend""",
    'description': """
        Batch Payslip Extend
    """,
    'version': '1.0',
    'depends': ['hr_payroll'],
    'data': [
        'views/hr_batch_payslip_view.xml'
    ],
    "price": 0.0,
    "currency": "EUR",
    'installable': True,
    'application': True,
    'auto_install': False,
}
