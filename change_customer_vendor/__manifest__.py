# -*- encoding: utf-8 -*-
{
    'name': "Customer <> Vendor",
    'version': '15.0.1.0.1',
    'summary': 'Set partner as customer or vendor',
    'category': 'Other',
    'description': """Set partner as customer or vendor""",
    "depends" : ['base'],
    'data': [
            'views/res_partner_view.xml',
             ],
    "images": [],
    'license': 'LGPL-3',

    'post_init_hook': '_update_fields_from_existing',
    'installable' : True,
    'application' : True,
    'auto_install' : False,
}
