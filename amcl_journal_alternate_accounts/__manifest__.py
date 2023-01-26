# -*- coding: utf-8 -*-

{
    'name': 'AMCL: Journal Alternate Accounts',
    'summary': """Journal Alternate Accounts""",
    'description': """
        Journal Alternate Accounts
    """,
    'version': '15.0.1.0.1',
    'author': 'AMCL',
    'depends': ['base','account_accountant'],
    'data': [
            'views/account_journal_view.xml',
            'views/account_payment_view.xml'
        ],
    "price": 0.0,
    "currency": "EUR",
    'installable': True,
    'application': True,
    'auto_install': False,
}
