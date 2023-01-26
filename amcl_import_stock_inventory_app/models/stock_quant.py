# -*- coding: utf-8 -*-
from odoo import fields, models


class StockQuant(models.Model):
	_inherit = 'stock.quant'

	def _get_inventory_move_values(self, qty, location_id, location_dest_id, out=False):
		res = super()._get_inventory_move_values(qty, location_id, location_dest_id, out)
		if self._context.get('inventory_date'):
			move_line_ids = res.get('move_line_ids')[0][2]
			move_line_ids.update({
				'date': self._context.get('inventory_date')
				})
			res.update({
				'date': self._context.get('inventory_date'),
				'move_line_ids': [(0, 0, move_line_ids)]
				})
		return res
