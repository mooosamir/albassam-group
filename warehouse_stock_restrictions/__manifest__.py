{
    'name': "Warehouse Restrictions",

    'summary': """
         Warehouse and Stock Location Restriction on Users.""",

    'description': """
        This Module Restricts the User from Accessing Warehouse and Process Stock Moves other than allowed to Warehouses and Stock Locations.
    """,

    'author': "odootec",

    'category': 'Warehouse',
    'version': '0.1',

    'depends': ['base', 'stock'],

    'data': [

        'users_view.xml',
        'security/security.xml', 
    ],
}
