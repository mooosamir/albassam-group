# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class HRContract(models.Model):
    _inherit = 'hr.contract'

    contract_element_line_ids = fields.One2many('hr.contract.element.line', 'contract_id', string='Contract Element Lines')

    def get_element_line(self, contract_elem_id):
        line_id = False
        for line in self.contract_element_line_ids:
            if line.contract_elem_conf_id.id == contract_elem_id.id:
                line_id = line
                break
        if line_id:
            return line_id
        else:
            raise ValidationError(_('Required Element "%s" not found from Contract Elements.'%(contract_elem_id.name)))


    @api.onchange('contract_element_line_ids')
    def set_emp_wage_from_lines(self):
        for line in self.contract_element_line_ids:
            if line.contract_elem_conf_id.code == 'BASIC':
                self.wage = line.amount
                break

    @api.constrains('contract_element_line_ids')
    def constrain_element_lines(self):
        line_contract_elem_ids = [line.contract_elem_conf_id.id for line in self.contract_element_line_ids]
        dup = {line.contract_elem_conf_id.name for line in self.contract_element_line_ids if line_contract_elem_ids.count(line.contract_elem_conf_id.id) > 1}
        if dup:
            raise ValidationError(_('Can not have multiple Contract Elements "%s"'%(', '.join(list(dup)))))
