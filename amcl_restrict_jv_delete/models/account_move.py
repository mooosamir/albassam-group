# -*- coding: utf-8 -*-
from odoo import models, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.ondelete(at_uninstall=False)
    def _unlink_except_posted(self):    
        if self.posted_before == True:
            raise UserError(_('Can not delete this entry. Journal Entry has been posted before.'))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
