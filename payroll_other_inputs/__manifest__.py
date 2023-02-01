# -*- coding: utf-8 -*-
{
    'name': "Payroll Other Inputs",
    'summary': """ """,
    'description': """ """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base','hr_payroll'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/payrol_other_input_views.xml',
        # 'views/templates.xml',
    ],
}
