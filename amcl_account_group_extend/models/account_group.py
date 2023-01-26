from odoo import fields, models


class AccountGroup(models.Model):
     _inherit = 'account.group'

     parent_id = fields.Many2one('account.group', index=True, ondelete='cascade', readonly=False)
     company_id = fields.Many2one('res.company', required=False, readonly=False)

     def _adapt_accounts_for_account_groups(self, account_ids=None):
          return True
          """Ensure consistency between accounts and account groups.

          Find and set the most specific group matching the code of the account.
          The most specific is the one with the longest prefixes and with the starting
          prefix being smaller than the account code and the ending prefix being greater.
          """
          company_ids = account_ids.company_id.ids if account_ids else self.company_id.ids
          account_ids = account_ids.ids if account_ids else []
          if not company_ids and not account_ids:
            return
          self.env['account.group'].flush(self.env['account.group']._fields)
          self.env['account.account'].flush(self.env['account.account']._fields)

          account_where_clause = ''
          where_params = [tuple(company_ids)]
          if account_ids:
            account_where_clause = 'AND account.id IN %s'
            where_params.append(tuple(account_ids))

          self._cr.execute(f'''
            WITH candidates_account_groups AS (
                SELECT
                    account.id AS account_id,
                    ARRAY_AGG(agroup.id ORDER BY char_length(agroup.code_prefix_start) DESC, agroup.id) AS group_ids
                FROM account_account account
                LEFT JOIN account_group agroup
                    ON agroup.code_prefix_start <= LEFT(account.code, char_length(agroup.code_prefix_start))
                    AND agroup.code_prefix_end >= LEFT(account.code, char_length(agroup.code_prefix_end))
                    AND agroup.company_id = account.company_id
                WHERE account.company_id IN %s {account_where_clause}
                GROUP BY account.id
            )
            UPDATE account_account
            SET group_id = rel.group_ids[1]
            FROM candidates_account_groups rel
            WHERE account_account.id = rel.account_id
          ''', where_params)
          self.env['account.account'].invalidate_cache(fnames=['group_id'])

     def _adapt_parent_account_group(self):
          return True
          """Ensure consistency of the hierarchy of account groups.

          Find and set the most specific parent for each group.
          The most specific is the one with the longest prefixes and with the starting
          prefix being smaller than the child prefixes and the ending prefix being greater.
          """
          if not self:
            return
          self.env['account.group'].flush(self.env['account.group']._fields)
          query = """
            WITH relation AS (
          SELECT DISTINCT FIRST_VALUE(parent.id) OVER (PARTITION BY child.id ORDER BY child.id, char_length(parent.code_prefix_start) DESC) AS parent_id,
                       child.id AS child_id
                  FROM account_group parent
                  JOIN account_group child
                    ON char_length(parent.code_prefix_start) < char_length(child.code_prefix_start)
                   AND parent.code_prefix_start <= LEFT(child.code_prefix_start, char_length(parent.code_prefix_start))
                   AND parent.code_prefix_end >= LEFT(child.code_prefix_end, char_length(parent.code_prefix_end))
                   AND parent.id != child.id
                   AND parent.company_id = child.company_id
                 WHERE child.company_id IN %(company_ids)s
            )
            UPDATE account_group child
               SET parent_id = relation.parent_id
              FROM relation
             WHERE child.id = relation.child_id;
          """
          self.env.cr.execute(query, {'company_ids': tuple(self.company_id.ids)})
          self.env['account.group'].invalidate_cache(fnames=['parent_id'])
          self.env['account.group'].search([('company_id', 'in', self.company_id.ids)])._parent_store_update()