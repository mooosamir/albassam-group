# -*- coding: utf-8 -*
from odoo import api, fields, models, tools


class CrmTeam(models.Model):
    _inherit = "crm.team"

    member_ids_om = fields.Many2many('res.users', 'sale_team_res_user_rel', 'user_id', 'sale_team_id', string='Member')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
