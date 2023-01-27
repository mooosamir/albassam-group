# -*- coding: utf-8 -*-

{
    'name': "Middle East Human Resource contract",
    'summary': """ Employee Contract ZHR *********""",
    'description': """ Additional features for hr_contract module according to SaudiArabia """,
    'author': 'ahcec',
    'website': "http://www.ahcec.com",
    'category': 'HR',
    'version': '1.5',
    'sequence': 20,
    'depends': ['base', 'hr_contract', 'amcl_hr_contract'],
    'data': [
        'security/security_data.xml',
        'security/ir.model.access.csv',
        'views/hr_contract_view.xml',
        'views/hr_contract_element_config_view.xml',
        'wizard/accrual_wizard_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
