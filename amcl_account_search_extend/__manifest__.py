# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    'name': 'AMCL: Account Search Extend',
    'summary': """Account Search Extend""",
    'description': """
        Account Search Extend
    """,
    'version': '1.0',
    'depends': ['base', 'account'],
    'data': [
        'views/journal_entry_view.xml',
    ],
    "price": 0.0,
    "currency": "EUR",
    'installable': True,
    'application': True,
    'auto_install': False,
}
