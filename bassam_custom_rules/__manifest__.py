# -*- coding: utf-8 -*-
{
    "name":"Bassam Custom Rules",
    "author": "Axis Technolabs",
    "version": "10.0.1.0",
    "website": "https://www.axistechnolabs.com/",
    "category": "Base",
    'summary': """
        Fix User Access issue of Product Category and Product UOM
    """,
    'description': """
        This module use to fix User Access issue of Product Category and Product UOM. 
    """,
    "depends": [
        "product",
        "sales_team",
        "sale"
        ],
    "data": [
        "views/product.xml",
        # "views/crm_team.xml",
    ],
    'demo': [],
    'test':[],
    'license': 'AGPL-3',
    'installable' : True,
    "auto_install" : False,
    "application" : True,
}
