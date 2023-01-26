# -*- coding: utf-8 -*-
{
    'name': "Multi-Company Access Rights",

    'summary': """
        Different access rights for multi-company users, Restriction, Restricted, Privillage, Restricted Menu, Different Access, Different Rights, Rights, Access Rights, Limited Access, Limited Menu""",

    'description': """
        Allow users to have different access rights in a multi-company environment
    """,

    'author': "Openinside",
    'website': "https://www.open-inside.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': "12.0.1.1.2",
    
    "license": "OPL-1",

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_users.xml',
        'views/res_users_groups.xml',
        'views/res_users_groups_wizard.xml',
        'views/actions.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        
    ],
    'odoo-apps' : True,
    "price" : 200,
    "currency": 'EUR',   
    'images':[
        'static/description/cover.png'
    ]       
}