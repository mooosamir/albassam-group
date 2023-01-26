from odoo import fields, models, api
from odoo.exceptions import ValidationError

class UserCompanyAccessWizard(models.TransientModel):
    _name = 'res.users.groups.wizard'
    _description = 'Multi Companies User Groups Wizard'
    
    @api.model
    def _group_domain(self):
        category_ids = self.env.ref("base.module_category_hidden")
        groups = self.env.ref("base.group_no_one") + self.env.ref("base.group_multi_company")
        return [('id', 'not in', groups.ids), ('category_id', 'not in', category_ids.ids)]        

    user_id = fields.Many2one('res.users', string='User', required=True, readonly=True)
    company_ids = fields.Many2many(related='user_id.company_ids', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True)
    group_ids = fields.Many2many('res.groups', domain = _group_domain)
    
    @api.model
    def default_get(self, fields_list):
        
        if self._context.get('default_user_id'):
            user = self.env['res.users'].browse(self._context.get('default_user_id'))
            if not user.has_group('base.group_multi_company') or len(user.company_ids) <=1:
                raise ValidationError("User is not have multi company access")            
        
        return super(UserCompanyAccessWizard, self).default_get(fields_list)
    
    @api.onchange('company_id', 'user_id')
    def onchange_company_id(self):
        if self.company_id and self.user_id:
            if self.user_id.company_group_ids:
                self.group_ids = self.user_id.company_group_ids.filtered(lambda a : self.company_id in a.company_ids).mapped('group_id')
            else:
                self.group_ids = self.env['res.groups'].search(self._group_domain() + [('id', 'in', self.user_id.groups_id.ids)])
    
    @api.onchange('group_ids')
    def _onchange_group_ids(self):
        if self.group_ids:
            for group in self.group_ids.mapped('trans_implied_ids'):
                if group not in self.group_ids:
                    self.group_ids += group
            
    
    def process(self):
        current_groups = self.user_id.company_group_ids.filtered(lambda a : self.company_id in a.company_ids).mapped('group_id')
        to_add = self.group_ids - current_groups
        to_remove = current_groups - self.group_ids
        
        for group in to_add:
            user_group = self.user_id.company_group_ids.filtered(lambda a : a.group_id == group)
            if not user_group:
                user_group = self.env['res.users.groups'].create({
                    'user_id': self.user_id.id,
                    'group_id': group.id})
                
            user_group.write({'company_ids' : [(4, self.company_id.id)]})
        
        for group in to_remove:
            user_group =self.user_id.company_group_ids.filtered(lambda a : a.group_id == group)
            user_group.write({'company_ids' : [(3, self.company_id.id)]})
            if not user_group.company_ids:
                user_group.unlink()
            
        self.user_id.update_user_access()
