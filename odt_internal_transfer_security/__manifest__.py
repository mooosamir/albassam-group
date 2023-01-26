# -*- coding: utf-8 -*-
{
    'name': "Stock Internal Transfer",

    'summary': """
        """,

    'description': """
        Internal Transfer with security access
    """,

    'author': "OdooTec",
    'website': "http://www.odootec.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Stock',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock','stock_operating_unit'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/internal_transfer_add_multiple_view.xml',
        'data/data.xml',
        'views/stock_transfer_view.xml',
        'report/report_internal_transfer_view.xml',
        'report/report.xml',

    ],

}
