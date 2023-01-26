from odoo import api, models

class Groups(models.Model):
    _inherit = 'res.groups'
    
    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        ids = super(Groups, self)._search(args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)
        
        if self._context.get('order_by_full_name'):
            ids = self.browse(ids).sorted(lambda group : (group.category_id.sequence if group.category_id else 999999 , group.full_name)).ids
        
        return ids



