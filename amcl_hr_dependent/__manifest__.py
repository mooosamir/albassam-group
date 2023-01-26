# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    'name': "AMCL : HR Dependent",
    'summary': "HR Dependent",
    'description': """ """,
    'author': 'AMCL',
    'category': 'HR',
    'version': '1.0',
    'depends': ['amcl_hr', 'res_documents'],
    'data': [
        'security/ir.model.access.csv',
        'views/amcl_hr_dependent.xml',
        ],
    'demo': [],
    'images': [],
    "price": 30.0,
    "currency": "EUR",
    'installable': True,
    'auto_install': False,
}
