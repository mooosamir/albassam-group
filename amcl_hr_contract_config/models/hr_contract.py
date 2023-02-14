# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class HRContract(models.Model):
    _inherit = 'hr.contract'

    contract_element_line_ids = fields.One2many('hr.contract.element.line', 'contract_id', string='Contract Element Lines')
    total_salary = fields.Float(string='Total Salary', compute='_get_total_salary')

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


    # @api.onchange('contract_element_line_ids')
    # def set_emp_wage_from_lines(self):
    #     for line in self.contract_element_line_ids:
    #         if line.contract_elem_conf_id.code == 'BASIC':
    #             self.wage = line.amount
    #             break

    @api.constrains('contract_element_line_ids')
    def constrain_element_lines(self):
        line_contract_elem_ids = [line.contract_elem_conf_id.id for line in self.contract_element_line_ids]
        dup = {line.contract_elem_conf_id.name for line in self.contract_element_line_ids if line_contract_elem_ids.count(line.contract_elem_conf_id.id) > 1}
        if dup:
            raise ValidationError(_('Can not have multiple Contract Elements "%s"'%(', '.join(list(dup)))))

    @api.depends('wage', 'signon_bonus_amount', 'remote_allow', 'ticket_monthly', 'contract_element_line_ids')
    def _get_total_salary(self):
        for contract in self:
            BASIC = contract.contract_element_line_ids.filtered(lambda line: line.code == 'BASIC').amount or 0.0
            ADD = contract.contract_element_line_ids.filtered(lambda line: line.code == 'ADD').amount or 0.0
            FOD = contract.contract_element_line_ids.filtered(lambda line: line.code == 'FOD').amount or 0.0
            HRA = contract.contract_element_line_ids.filtered(lambda line: line.code == 'HRA').amount or 0.0
            INT = contract.contract_element_line_ids.filtered(lambda line: line.code == 'INT').amount or 0.0
            MFL = contract.contract_element_line_ids.filtered(lambda line: line.code == 'MFL').amount or 0.0
            MOB = contract.contract_element_line_ids.filtered(lambda line: line.code == 'MOB').amount or 0.0
            RPP = contract.contract_element_line_ids.filtered(lambda line: line.code == 'RPP').amount or 0.0
            RSO = contract.contract_element_line_ids.filtered(lambda line: line.code == 'RSO').amount or 0.0
            RTFI = contract.contract_element_line_ids.filtered(lambda line: line.code == 'RTFI').amount or 0.0
            SEN = contract.contract_element_line_ids.filtered(lambda line: line.code == 'SEN').amount or 0.0
            SPC = contract.contract_element_line_ids.filtered(lambda line: line.code == 'SPC').amount or 0.0
            SUP = contract.contract_element_line_ids.filtered(lambda line: line.code == 'SUP').amount or 0.0
            TA = contract.contract_element_line_ids.filtered(lambda line: line.code == 'TA').amount or 0.0
            UT_UT = contract.contract_element_line_ids.filtered(lambda line: line.code == 'UT/UT').amount or 0.0

            contract.wage = BASIC + \
                            ADD + FOD + INT + MFL + MOB + RPP + \
                            RSO + RTFI + SEN + SPC + SUP + UT_UT+ \
                            contract.signon_bonus_amount + \
                            HRA + TA + \
                            contract.other_allow + \
                            contract.remote_allow + \
                            contract.ticket_monthly
            contract.total_salary = BASIC + \
                            ADD + FOD + INT + MFL + MOB + RPP + \
                            RSO + RTFI + SEN + SPC + SUP + UT_UT+ \
                            contract.signon_bonus_amount + \
                            HRA + TA + \
                            contract.other_allow + \
                            contract.remote_allow + \
                            contract.ticket_monthly
