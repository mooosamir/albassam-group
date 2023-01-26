# -*- coding: utf-8 -*-
import time

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockTransfer(models.Model):
    _name = 'stock.transfer.internal'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'utm.mixin']

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        self.env['ir.rule'].sudo().browse(
            self.env.ref('stock_operating_unit.ir_rule_stock_warehouse_allowed_operating_units').id).sudo().write(
            {'domain_force': "[(1,'=',1)]"})
        self.env['ir.rule'].sudo().browse(
            self.env.ref('stock_operating_unit.ir_rule_stock_picking_type_allowed_operating_units').id).sudo().write(
            {'domain_force': "[(1,'=',1)]"})
        self.env['ir.rule'].sudo().browse(
            self.env.ref('stock_operating_unit.ir_rule_stock_location_allowed_operating_units').id).sudo().write(
            {'domain_force': "[(1,'=',1)]"})

        fields = super(StockTransfer, self).search_read(domain=domain, fields=fields, offset=0, limit=offset,
                                                        order=order)
        return fields

    @api.model
    def _default_domain(self):
        list_ou = []
        for ou in self.env.user.operating_unit_ids:
            list_ou.append(ou.id)
        return [('usage', '=', 'internal'),('operating_unit_id', 'in', list_ou)]

    # @api.model
    # def _default_domain_dest(self):
    #     return "[('usage', '=', 'internal'),('operating_unit_id', 'not in', [" + str(
    #         self.env.user.default_operating_unit_id.id) + "])]"

    @api.model
    def _default_domain_dest(self):
        return [('usage', '=', 'internal')]

    # @api.model
    # def _default_domain_picking(self):
    #     return "[('code', '=', 'internal'),('warehouse_id.operating_unit_id', 'not in', [" + str(
    #         self.env.user.default_operating_unit_id.id) + "])]"

    @api.model
    def _default_domain_picking(self):
        if self.env.user.id != 1 or not self.env.user.has_group('stock.group_stock_manager'):
            list_domain = []
            for type in self.env.user.default_picking_type_ids:
                list_domain.append(type.id)
            return [('code', '=', 'internal'), ('id', 'in', list_domain)]

    @api.model
    def _get_user_domain(self):
        return [('id','=',self.env.user.id)]

    # @api.model
    @api.onchange('location_dest_id')
    def _get_to_user_domain(self):
        if self.location_dest_id:
            obj = self.env['res.users'].search([('default_operating_unit_id','=',self.location_dest_id.operating_unit_id.id)])
            list_users = []
            for user in obj:
                list_users.append(user.id)
            return {'domain':{'to_user':[('id','in',list_users)]}}
    source_doc = fields.Char(string='Source Document',tracking=True)
    name = fields.Char(string='Name', readonly=True,
                       default=lambda obj: obj.env['ir.sequence'].next_by_code('stock.internal.transfer'),tracking=True)
    picking_type_id = fields.Many2one(comodel_name='stock.picking.type', string='Picking Type', required=True,
                                      tracking=True)
    location_id = fields.Many2one(comodel_name='stock.location', string='From Location', required=True,
                                  tracking=True)
    location_dest_id = fields.Many2one(comodel_name='stock.location', string='To Location', required=True,
                                       domain=lambda self: self._default_domain_dest(),tracking=True)
    user_id = fields.Many2one(comodel_name='res.users', string='By', domain=_get_user_domain,
                              default=lambda self: self.env.user.id,tracking=True)
    lines = fields.One2many(comodel_name='product.transfer.line', inverse_name='transfer_id',
                            string='Transfer Products',tracking=True)
    to_user = fields.Many2one(comodel_name="res.users", string="Send to", required=True,tracking=True )
    date = fields.Datetime(string='Date', required=True, default=fields.Datetime.now(),tracking=True)
    state = fields.Selection(selection=[('cancel', 'Cancel'), ('draft', 'Draft'), ('send', 'Send'), ('done', 'Done')],
                             string='Status', default='draft',tracking=True)
    picking_ids = fields.One2many(comodel_name='stock.picking', inverse_name='transfer_id_new', string='Picking',tracking=True)

    
    def action_cancel(self):
        self.write({'state': 'cancel'})
        return True

    @api.model
    def create(self, vals):
        if not vals.get('lines'):
            raise UserError(_("You can't save empty transfer."))
        res = super(StockTransfer, self.sudo()).create(vals)
        self.env['ir.rule'].sudo().browse(
            self.env.ref('stock_operating_unit.ir_rule_stock_warehouse_allowed_operating_units').id).sudo().write(
            {
                'domain_force': "['|', ('operating_unit_id','=',False),('operating_unit_id','in',user.operating_unit_ids.ids)]"})
        self.env['ir.rule'].sudo().browse(
            self.env.ref('stock_operating_unit.ir_rule_stock_picking_type_allowed_operating_units').id).sudo().write(
            {
                'domain_force': "['|', ('warehouse_id.operating_unit_id','=',False),('warehouse_id.operating_unit_id','in',user.operating_unit_ids.ids)]"})
        self.env['ir.rule'].sudo().browse(
            self.env.ref('stock_operating_unit.ir_rule_stock_location_allowed_operating_units').id).sudo().write(
            {
                'domain_force': "['|', ('operating_unit_id', '=', False),('operating_unit_id', 'in', user.operating_unit_ids.ids)]"})

        return res

    
    def write(self, vals):
        res = super(StockTransfer, self.sudo()).write(vals)
        self.env['ir.rule'].sudo().browse(
            self.env.ref('stock_operating_unit.ir_rule_stock_warehouse_allowed_operating_units').id).sudo().write(
            {
                'domain_force': "['|', ('operating_unit_id','=',False),('operating_unit_id','in',user.operating_unit_ids.ids)]"})
        self.env['ir.rule'].sudo().browse(
            self.env.ref('stock_operating_unit.ir_rule_stock_picking_type_allowed_operating_units').id).sudo().write(
            {
                'domain_force': "['|', ('warehouse_id.operating_unit_id','=',False),('warehouse_id.operating_unit_id','in',user.operating_unit_ids.ids)]"})
        self.env['ir.rule'].sudo().browse(
            self.env.ref('stock_operating_unit.ir_rule_stock_location_allowed_operating_units').id).sudo().write(
            {
                'domain_force': "['|', ('operating_unit_id', '=', False),('operating_unit_id', 'in', user.operating_unit_ids.ids)]"})

        return res

    
    def action_cancel_manager(self):
        picking_vals = {
            'picking_type_id': self.env['stock.picking.type'].sudo().browse(self.picking_type_id.id).id,
            'date': self.date,
            'transfer_id_new': self.id,
            'location_id': self.env['stock.location'].sudo().browse(self.location_dest_id.id).id,
            'operating_unit_id': self.env['operating.unit'].sudo().browse(
                self.env['stock.location'].sudo().browse(self.location_dest_id.id).operating_unit_id.id).id,
            'location_dest_id': self.env['stock.location'].sudo().browse(self.location_id.id).id,
            'origin': self.name,
        }
        new_picking = self.env['stock.picking'].sudo().create(picking_vals)

        for record in self.lines:
            self.env['stock.move'].sudo().create({
                'name': self.name,
                'product_id': record.product_id.id,
                'product_uom_qty': record.product_qty,
                'product_uom': record.product_id.uom_id and record.product_id.uom_id.id or False,
                'picking_id': new_picking.id,
                'location_id': self.env['stock.location'].sudo().browse(self.location_dest_id.id).id,
                'location_dest_id': self.env['stock.location'].sudo().browse(self.location_id.id).id})
        new_picking.action_assign()
        new_picking.do_prepare_partial()
        new_picking.force_assign()
        new_picking.do_transfer()
        self.write({'state': 'done'})
        self.write({'state': 'cancel'})
        return True

    
    def action_draft(self):
        self.write({'state': 'draft'})
        return True

    
    def action_send(self):
        for line in self.sudo().lines:
            qty_av = line.product_id.with_context(
                {'location': self.env['stock.location'].sudo().browse(self.location_id.id).id}).qty_available
            final_qty = qty_av - line.product_qty
            if qty_av <= 0:
                raise UserError(_('Problem With Sending\n'
                                'Product " %s " has " %s " qty in" %s "and you are trying to transfer %s') % (
                                  line.product_id.name, qty_av,
                                  self.env['stock.location'].sudo().browse(self.location_id.id).complete_name,
                                  line.product_qty))
            elif final_qty < 0:
                raise UserError(_('Please check the item balance in the branch ..  برجاء مراجعه رصيد الصنف في الفرع'))
        if self.to_user:
            mail = self.env['mail.thread']
            post_vars = {'subject': "Approve The Incoming Transfer",
                         'body': "Incoming Transfer ( " + str(self.name) + " ) Should be approved by you to accept it"}
            mail.message_post(type="notification", partner_ids=[self.to_user.partner_id.id],
                              subtype="mt_comment", **post_vars)
        self.write({'state': 'send'})
        return True

    
    def action_receive(self):
        if self.env.user.id != self.to_user.id:
            raise UserError(_('You are not the approver of this Transfer'))
        for line in self.sudo().lines:
            qty_av = line.product_id.with_context(
                {'location': self.env['stock.location'].sudo().browse(self.location_id.id).id}).qty_available
            if qty_av <= 0:
                raise UserError(_('Problem With Sending\n'
                                'Product " %s " has " %s " qty in" %s "and you are trying to transfer %s') % (
                                  line.product_id.name, qty_av,
                                  self.env['stock.location'].sudo().browse(self.location_id.id).complete_name,
                                  line.product_qty))

        if self.env['stock.location'].sudo().browse(
                self.location_dest_id.id).operating_unit_id.id != self.env.user.default_operating_unit_id.id:
            raise UserError(_('Problem With Approving\n'
                            'You do not have access to the destination location'))
        picking_vals = {
            'picking_type_id': self.env['stock.picking.type'].sudo().browse(self.picking_type_id.id).id,
            'date': self.date,
            'transfer_id_new': self.id,
            'location_id': self.env['stock.location'].sudo().browse(self.location_id.id).id,
            'operating_unit_id': self.env['operating.unit'].sudo().browse(
                self.env['stock.location'].sudo().browse(self.location_dest_id.id).operating_unit_id.id).id,
            'location_dest_id': self.env['stock.location'].sudo().browse(self.location_dest_id.id).id,
            'origin': self.name,
        }
        new_picking = self.env['stock.picking'].sudo().create(picking_vals)

        for record in self.lines:
            self.env['stock.move'].sudo().create({
                'name': self.name,
                'product_id': record.product_id.id,
                'product_uom_qty': record.product_qty,
                'product_uom': record.product_id.uom_id and record.product_id.uom_id.id or False,
                'picking_id': new_picking.id,
                'location_id': self.env['stock.location'].sudo().browse(self.location_id.id).id,
                'location_dest_id': self.env['stock.location'].sudo().browse(self.location_dest_id.id).id})
        new_picking.action_assign()
        new_picking.do_prepare_partial()
        new_picking.force_assign()
        new_picking.do_transfer()
        self.write({'state': 'done'})
        return True

    
    def unlink(self):
        for move in self:
            if move.state in ('send', 'done', 'cancel'):
                raise UserError(_('You can only delete in draft state.'))

        return super(StockTransfer, self).unlink()


StockTransfer()


class StockTransferLine(models.Model):
    _name = 'product.transfer.line'

    transfer_id = fields.Many2one(comodel_name='stock.transfer.internal')
    product_id = fields.Many2one(comodel_name='product.product', string='Product', required=True)
    product_qty = fields.Float(string='Qty', required=True, default=1.0)
    product_uom_id = fields.Many2one(comodel_name='uom.uom', string='Unit of Measure', required=False,
                                     invisible=True)

    
    @api.onchange('product_id')
    def onchange_product_id(self):
        if not self.product_id:
            self.product_uom_id = False
        else:
            self.product_uom_id = self.product_id.uom_id and self.product_id.uom_id.id or False


StockTransferLine()


class StockPicking(models.Model):
    _inherit = "stock.picking"

    transfer_id_new = fields.Many2one(comodel_name='stock.transfer.internal', string='Transfer')

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        self.env['ir.rule'].sudo().browse(
            self.env.ref('stock_operating_unit.ir_rule_stock_warehouse_allowed_operating_units').id).sudo().write(
            {
                'domain_force': "['|', ('operating_unit_id','=',False),('operating_unit_id','in',user.operating_unit_ids.ids)]"})
        self.env['ir.rule'].sudo().browse(
            self.env.ref('stock_operating_unit.ir_rule_stock_picking_type_allowed_operating_units').id).sudo().write(
            {
                'domain_force': "['|', ('warehouse_id.operating_unit_id','=',False),('warehouse_id.operating_unit_id','in',user.operating_unit_ids.ids)]"})
        self.env['ir.rule'].sudo().browse(
            self.env.ref('stock_operating_unit.ir_rule_stock_location_allowed_operating_units').id).sudo().write(
            {
                'domain_force': "['|', ('operating_unit_id', '=', False),('operating_unit_id', 'in', user.operating_unit_ids.ids)]"})

        fields = super(StockPicking, self).search_read(domain=domain, fields=fields, offset=0, limit=offset,
                                                       order=order)
        return fields


StockPicking()


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        self.env['ir.rule'].sudo().browse(
            self.env.ref('stock_operating_unit.ir_rule_stock_warehouse_allowed_operating_units').id).sudo().write(
            {
                'domain_force': "['|', ('operating_unit_id','=',False),('operating_unit_id','in',user.operating_unit_ids.ids)]"})
        self.env['ir.rule'].sudo().browse(
            self.env.ref('stock_operating_unit.ir_rule_stock_picking_type_allowed_operating_units').id).sudo().write(
            {
                'domain_force': "['|', ('warehouse_id.operating_unit_id','=',False),('warehouse_id.operating_unit_id','in',user.operating_unit_ids.ids)]"})
        self.env['ir.rule'].sudo().browse(
            self.env.ref('stock_operating_unit.ir_rule_stock_location_allowed_operating_units').id).sudo().write(
            {
                'domain_force': "['|', ('operating_unit_id', '=', False),('operating_unit_id', 'in', user.operating_unit_ids.ids)]"})

        fields = super(StockPickingType, self).search_read(domain=domain, fields=fields, offset=0, limit=offset,
                                                           order=order)
        return fields


StockPickingType()

