# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    'name': "AMCL : IQAMA Management",
    'summary': """HR IQAMA Management """,
    'description': """
    IQAMA register and notify when near to expiry.
    """,
    'author': 'AMCL',
    'category': 'Generic Modules/Human Resources',
    'version': '1.0',
    'depends': ['amcl_hr_dependent'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/cron.xml',
        # 'data/email_template_data.xml',
        'views/hr_iqama_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/iqama_demo.xml'
    ],
    'images': [
        'static/description/main_screen.jpg'
    ],
    "price": 149.0,
    "currency": "EUR",
    'installable': True,
    'application': True,
    'auto_install': False,
}
