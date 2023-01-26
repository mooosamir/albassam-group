# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    'name': "AMCL : GOSI Contribution",
    'summary': """ahcec HR GOSI Contribution""",
    'description': """
        By this module we can calculate GOSI of employee and can deduct the amount from employee payslip.
    """,
    'author': 'AMCL',
    'category': 'Generic Modules/Human Resources',
    'version': '1.0',
    'depends': ['amcl_hr', 'hr_payroll', 'amcl_hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        # 'data/hr_payroll_data.xml',
        'views/hr_employee_gosi_view.xml',
        'views/hr_payroll_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/employee_gosi_demo.xml',
    ],
    'images': [
        'static/description/main_screen.jpg'
    ],
    "price": 250.0,
    "currency": "EUR",
    'installable': True,
    'application': True,
    'auto_install': False,
}
