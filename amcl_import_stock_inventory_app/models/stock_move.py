from odoo import fields, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    def write(self, vals):
        if self._context.get('inventory_date'):
            vals.update({
                'date': self._context.get('inventory_date')
                })
        res = super().write(vals)
        return res

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def write(self, vals):
        if self._context.get('inventory_date'):
            vals.update({
                'date': self._context.get('inventory_date')
                })
        res = super().write(vals)
        return res
