from odoo import fields, models


class ProductTemplate(models.Model):
	_inherit = 'product.template'

	categ_id = fields.Many2one(
        'product.category', 'Product Category',
        change_default=True, group_expand='_read_group_categ_id',
        required=True, help="Select category for the current product", default=False)
