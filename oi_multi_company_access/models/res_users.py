from odoo import api, fields, models

class Users(models.Model):
    _inherit = 'res.users'

    company_group_ids = fields.One2many('res.users.groups', 'user_id', string='Multi Companies Groups')
    show_multi_company_access = fields.Boolean(compute = '_calc_show_multi_company_access')
    
    
    def get_groups(self, company_id):
        if self.company_group_ids:
            group_ids = self.company_group_ids.filtered(lambda a : company_id in a.company_ids).mapped('group_id')
            group_ids |= self.env.ref('base.group_user')
            group_ids |= self.env.ref('base.group_multi_company')
            group_ids |= group_ids.mapped('trans_implied_ids')
            return group_ids
        
        return self.groups_id
                
    
    def write(self, vals):
        res = super(Users, self).write(vals)
        if 'company_id' in vals or 'company_group_ids' in vals:
            for record in self.sudo():
                record.update_user_access()
        return res
    
    
    def update_user_access(self):
        if self.company_group_ids:
            self.write({'groups_id' : [(6, False, self.get_groups(self.company_id).ids)]})
            
    
    @api.depends('company_ids', 'groups_id')
    def _calc_show_multi_company_access(self):
        group_user = self.env.ref('base.group_user')
        group_multi_company = self.env.ref('base.group_multi_company')
        for record in self:
            record.show_multi_company_access = group_user in record.groups_id and group_multi_company in record.groups_id and len(record.company_ids) > 1