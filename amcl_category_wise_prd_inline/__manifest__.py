# -*- encoding: utf-8 -*-
{
    'name': "Category Wise Product Inline",
    'version': '13.0.1.0.1',
    'summary': 'Category Wise Product Inline',
    'category': 'Other',
    'description': """Category Wise Product Inline""",
    "depends" : ['base', 'stock','sale_management', 'product'],
    'data': [
            'views/product_category_view.xml',
            'views/sale_view.xml',
             ],
    'license': 'LGPL-3',

    'installable' : True,
    'application' : True,
    'auto_install' : False,
}
