from odoo import fields, models, api

class UserCompanyAccess(models.Model):
    _name = 'res.users.groups'
    _description = 'Multi Companies User Groups'

    group_id = fields.Many2one('res.groups', string='Group', required=True)
    user_id = fields.Many2one('res.users', string='User', required=True)
    company_ids = fields.Many2many('res.company', string='Companies')

    _sql_constraints = [ 
        ('unique_access', 'unique(user_id, group_id)', 'Duplicate Group')
        ]

    
    
    def name_get(self):
        res = []
        for record in self:
            name = "%s - %s" % (record.user_id.display_name, record.group_id.display_name)
            res.append((record.id, name))
        return res