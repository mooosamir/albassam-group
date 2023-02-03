# -*- coding: utf-8 -*-

{
    'name': 'Retention',
    'version': '15.0.1.0.0',
    'summary': """""",
    'description': '',
    'category': 'Accounting',
    'author': 'AMCL',
    'company': '',
    'website': "",
    'depends': ['sale_management', 'account', 'account_asset'],
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',        
        'views/view.xml',
        'views/retention_view.xml',
    ],
    'demo': [
    ],
    'images': [],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}

