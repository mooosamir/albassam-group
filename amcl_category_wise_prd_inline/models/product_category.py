from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    show_product_in_salelines = fields.Boolean(string="Show Product In SaleLines")


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def name_search(self, name='', args=None, operator='=', limit=100):
        args = args or []
        if self._context.get('filter_by_category'):
            product_ids = self.env['product.product'].search([('categ_id.show_product_in_salelines','=',True)])
            args += [('id','in',product_ids.ids)]
        return super(ProductProduct,self).name_search(name, args, operator, limit)
