# -*- coding: utf-8 -*-

{
    'name': "AMCL : Middle East HR contract",
    'summary': """ Middle East Employee Contract""",
    'description': """ Additional features for hr_contract module according to SaudiArabia """,
    'author': 'AMCL',
    'category': 'HR',
    'version': '1.5',
    'sequence': 20,
    'depends': ['account', 'hr_contract', 'hr_payroll', 'hr', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'data/hr_payroll_data.xml',
        'views/contract_view.xml',
        'views/hr_accrual_view.xml',
        'wizard/accrual_wizard_view.xml',
        'views/contract_cron.xml',
        'report/empcontract_report_qweb.xml',
        'report/newjoin_empcontract_reportqweb.xml',
        'register_qweb_report.xml',
        'menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
