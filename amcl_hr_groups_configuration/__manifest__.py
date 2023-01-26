# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "AMCL : Groups Configuration",
    'summary': """ Middle East Human Resource """,
    'description': """
            Middle East Human Resource Groups Configuration
        """,
    'author': 'ahcec',
    'website': 'http://www.ahcec.com',
    'category': 'Human Resources',
    'version': '1.0',
    'sequence': 20,
    'depends': ['base', 'amcl_hr_branch'],
    # 'depends': [],
    'data': [
        'security/ir.model.access.csv',
        # 'views/hr_branch_view.xml',
        'views/hr_groups_configuration_view.xml',
        # 'menu.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
#         'demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}