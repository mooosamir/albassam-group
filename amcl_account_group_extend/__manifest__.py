# -*- coding: utf-8 -*-
{
    'name': 'AMCL: Account Group',
    'version': '15.0.1.0.1',
    'author': 'AMCL',
    'description': """
        Account group
    """,
    'summary': """
        Account group
    """,
    'depends': [
        'base', 'account'
    ],
    'data': [
        'security/security.xml',
        'views/account_group_view.xml',
    ],
    "images": [],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
