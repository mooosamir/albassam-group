# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
# from odoo.exceptions import Warning

class ResUsers(models.Model):
    _inherit = 'res.users'

    restrict_locations = fields.Boolean('Restrict Location')

    stock_location_ids = fields.Many2many(
        'stock.location',
        'location_security_stock_location_users',
        'user_id',
        'location_id',
        'Stock Locations')

    default_picking_type_ids = fields.Many2many(
        'stock.picking.type', 'stock_picking_type_users_rel',
        'user_id', 'picking_type_id', string='Default Warehouse Operations')


class stock_move(models.Model):
    _inherit = 'stock.move'

    # 
    # @api.constrains('state', 'location_id', 'location_dest_id')
    # def check_user_location_rights(self):
    #     if self.state == 'draft':
    #         return True
    #     user_locations = self.env.user.stock_location_ids
    #     if self.env.user.restrict_locations:
    #         message = _(
    #             'Invalid Location. You cannot process this move since you do '
    #             'not control the location "%s". '
    #             'Please contact your Adminstrator.')
    #         if self.location_id not in user_locations:
    #             raise Warning(message % self.location_id.name)
    #         elif self.location_dest_id not in user_locations:
    #             raise Warning(message % self.location_dest_id.name)


class Stock(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def _default_domain(self):
        if self.env.user.id != 1:
            list_domain = []
            for location in self.env.user.stock_location_ids:
                print("----------------------------",location.name)
                list_domain.append(location.id)

            domain = [('id', 'in', list_domain)]
            print("=================================", list_domain)
            return domain

    location_id = fields.Many2one(
        'stock.location', "Source Location Zone",
        default=lambda self: self.env['stock.picking.type'].browse(
            self._context.get('default_picking_type_id')).default_location_src_id,
        readonly=True, required=True,domain=lambda self: self._default_domain(),
        states={'draft': [('readonly', False)]})

    location_dest_id = fields.Many2one(
        'stock.location', "Destination Location Zone",
        default=lambda self: self.env['stock.picking.type'].browse(
            self._context.get('default_picking_type_id')).default_location_dest_id,
        readonly=True, required=True, domain=lambda self: self._default_domain(),
        states={'draft': [('readonly', False)]})	
