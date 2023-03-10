import datetime
from collections import defaultdict
from markupsafe import Markup
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero, plaintext2html
import logging

_logger = logging.getLogger(__name__)

debit_type_account_field_string = {
    'employee': 'Debit Account',
    'operator': 'Operation Debit Account',
    'sale_marketing': 'Sales & Marketing Debit Account',
}

credit_type_account_field_string = {
    'employee': 'Credit Account',
    'operator': 'Operation Credit Account',
    'sale_marketing': 'Sales & Marketing Credit Account',
}


class SalaryRulesInherit(models.Model):
    _inherit = 'hr.salary.rule'

    journal = fields.Boolean('New Journal')
    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal')

    project_account_debit = fields.Many2one('account.account', 'Operation Debit Account',
                                            domain=[('deprecated', '=', False)])
    project_account_credit = fields.Many2one('account.account', 'Operation Credit Account',
                                             domain=[('deprecated', '=', False)])

    sale_marketing_account_debit_id = fields.Many2one('account.account', 'Sales & Marketing Debit Account',
                                            domain=[('deprecated', '=', False)])
    sale_marketing_account_credit_id = fields.Many2one('account.account', 'Sales & Marketing Credit Account',
                                             domain=[('deprecated', '=', False)])


class HrPayslipLineInherit(models.Model):
    _inherit = 'hr.payslip.line'

    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal')

    def add_line_in_jv(self):
        # if the lines has seperate journal_id selected then for that line amount we will create Separate JV
        # And Will not add this line into current JV creation
        if not self.journal_id:
            return True
        else:
            return False

    def validate_rule_for_batch(self):
        # this method will be called when batch payslips are being DONE, And Creating draft entry
        # If the rule has Boolean journal true then raise warning
        if self.salary_rule_id.journal:
            raise ValidationError(_("Invalid '%s' line in '%s' payslip."%(self.name,self.slip_id.number)))

    def get_jv_accounts(self):
        debit_account_id = False
        credit_account_id = False
        if self.employee_id.type_of_employee == 'operator':
            debit_account_id = self.salary_rule_id.project_account_debit.id
            credit_account_id = self.salary_rule_id.project_account_credit.id
        elif self.employee_id.type_of_employee == 'sale_marketing':
            debit_account_id = self.salary_rule_id.sale_marketing_account_debit_id.id
            credit_account_id = self.salary_rule_id.sale_marketing_account_credit_id.id
        else:
            debit_account_id = self.salary_rule_id.account_debit.id
            credit_account_id = self.salary_rule_id.account_credit.id

        return debit_account_id,credit_account_id


class HrPayslipInherit(models.Model):
    _inherit = 'hr.payslip'

    move_ids = fields.One2many(
        comodel_name='account.move', inverse_name='payslip_id', string='Moves')

    def _prepare_line_values(self, line, account_id, date, debit, credit):
        analytic_account = False
        if self.payslip_run_id.group_by_analytic_account:
            analytic_account = line.salary_rule_id.analytic_account_id.id or line.slip_id.contract_id.analytic_account_id.id
            if line.employee_id.analytic_account_id:
                analytic_account = line.employee_id.analytic_account_id.id

        values = {
            'name': line.name,
            'partner_id': line.partner_id.id,
            'account_id': account_id,
            'journal_id': line.slip_id.struct_id.journal_id.id,
            'date': date,
            'debit': debit,
            'credit': credit,
            'analytic_account_id': analytic_account,
        }
        if line.salary_rule_id.code == 'LOAN' and line.employee_id.address_home_id and credit > 0:
            values.update({
                'partner_id': line.employee_id.address_home_id.id
                })
        return values

    def compute_sheet(self):
        res = super(HrPayslipInherit, self).compute_sheet()
        for line in self.line_ids:
            if line.salary_rule_id.journal:
                line.write({'journal_id': line.salary_rule_id.journal_id})
        return res

    def action_payslip_done(self):
        res = super(HrPayslipInherit, self).action_payslip_done()

        date = fields.date.today()

        for line in self.line_ids:
            ids = []
            if line.journal_id:
                _logger.critical('*== I am here ==*')
                debit_dic = {
                    'name': line.name + '-' + line.employee_id.name,
                    'partner_id': False,
                    'account_id': line.salary_rule_id.account_debit.id,
                    'journal_id': line.journal_id.id,
                    'date': date,
                    'debit': abs(line.total),
                    'credit': 0.0
                }
                ids.append((0, 0, debit_dic))
                credit_dic = {
                    'name': line.name + '-' + line.employee_id.name,
                    'partner_id': False,
                    'account_id': line.salary_rule_id.account_credit.id,
                    'journal_id': line.journal_id.id,
                    'date': date,
                    'debit': 0.0,
                    'credit': abs(line.total)
                }
                ids.append((0, 0, credit_dic))
                # ids.append(credit_dic)
                move = self.env['account.move'].sudo().create({
                    'name': '/',
                    'payslip_id': self.id,
                    'move_type': 'entry',
                    'ref': line.employee_id.name,
                    'journal_id': line.journal_id.id,
                    'date': date,
                    'line_ids': ids
                })


            # self.gosi_move_id = move.id
        return res

    def _action_create_account_move(self):

        # self._action_create_account_move()
        precision = self.env['decimal.precision'].precision_get('Payroll')

        # Add payslip without run
        payslips_to_post = self.filtered(lambda slip: not slip.payslip_run_id)

        # Adding pay slips from a batch and deleting pay slips with a batch that is not ready for validation.
        payslip_runs = (self - payslips_to_post).mapped('payslip_run_id')
        for run in payslip_runs:
            if run._are_payslips_ready():
                payslips_to_post |= run.slip_ids

        # A payslip need to have a done state and not an accounting move.
        payslips_to_post = payslips_to_post.filtered(lambda slip: slip.state == 'done' and not slip.move_id)

        # Check that a journal exists on all the structures
        if any(not payslip.struct_id for payslip in payslips_to_post):
            raise ValidationError(_('One of the contract for these payslips has no structure type.'))
        if any(not structure.journal_id for structure in payslips_to_post.mapped('struct_id')):
            raise ValidationError(_('One of the payroll structures has no account journal defined on it.'))

        # Map all payslips by structure journal and pay slips month.
        # {'journal_id': {'month': [slip_ids]}}
        slip_mapped_data = defaultdict(lambda: defaultdict(lambda: self.env['hr.payslip']))

        for slip in payslips_to_post:
            slip_mapped_data[slip.struct_id.journal_id.id][fields.Date().end_of(slip.date_to, 'month')] |= slip
        for journal_id in slip_mapped_data:  # For each journal_id.
            for slip_date in slip_mapped_data[journal_id]:  # For each month.
                line_ids = []
                debit_sum = 0.0
                credit_sum = 0.0
                date = slip_date
                employee_id = False
                if not self.payslip_run_id:
                    employee_id = slip.employee_id.id
                move_dict = {
                    'narration': '',
                    'ref': str(date.strftime("%B-%Y")),
                    'journal_id': journal_id,
                    'payslip_employee_id': employee_id,
                    'date': date,
                }

                for slip in slip_mapped_data[journal_id][slip_date]:
                    move_dict['narration'] += plaintext2html(slip.number or '' + ' - ' + slip.employee_id.name or '')
                    move_dict['narration'] += Markup('<br/>')
                    for line in slip.line_ids.filtered(lambda line: line.category_id and line.add_line_in_jv()):
                        # Validate the line rule else raise error so the user can see which line is having an issue
                        line.validate_rule_for_batch()
                        if not line.journal_id:
                            amount = abs(line.total)
                            if line.code == 'NET':  # Check if the line is the 'Net Salary'.
                                for tmp_line in slip.line_ids.filtered(lambda line: line.category_id):
                                    if tmp_line.salary_rule_id.not_computed_in_net:  # Check if the rule must be computed in the 'Net Salary' or not.
                                        if amount > 0:
                                            amount -= abs(tmp_line.total)
                                        elif amount < 0:
                                            amount += abs(tmp_line.total)
                            if float_is_zero(amount, precision_digits=precision):
                                continue

                            debit_account_id, credit_account_id = line.get_jv_accounts()
                            # instead of below code to select pair of accounts we will call a method to select and rasie validation error if the accounts are not there

                            # debit_account_id = line.salary_rule_id.account_debit.id
                            # credit_account_id = line.salary_rule_id.account_credit.id

                            if debit_account_id:  # If the rule has a debit account.
                                debit = amount if amount > 0.0 else 0.0
                                credit = -amount if amount < 0.0 else 0.0

                                debit_line = self._get_existing_lines(
                                    line_ids, line, debit_account_id, debit, credit)

                                if not debit_line:
                                    debit_line = self._prepare_line_values(line, debit_account_id, date, debit, credit)
                                    debit_line['tax_ids'] = [(4, tax_id) for tax_id in
                                                             line.salary_rule_id.account_debit.tax_ids.ids]
                                    line_ids.append(debit_line)
                                else:
                                    debit_line['debit'] += debit
                                    debit_line['credit'] += credit

                            if credit_account_id:  # If the rule has a credit account.
                                debit = -amount if amount < 0.0 else 0.0
                                credit = amount if amount > 0.0 else 0.0
                                credit_line = self._get_existing_lines(
                                    line_ids, line, credit_account_id, debit, credit)

                                if not credit_line:
                                    credit_line = self._prepare_line_values(line, credit_account_id, date, debit,
                                                                            credit)
                                    credit_line['tax_ids'] = [(4, tax_id) for tax_id in
                                                              line.salary_rule_id.account_credit.tax_ids.ids]
                                    line_ids.append(credit_line)
                                else:
                                    credit_line['debit'] += debit
                                    credit_line['credit'] += credit
                for line_id in line_ids:  # Get the debit and credit sum.
                    debit_sum += line_id['debit']
                    credit_sum += line_id['credit']

                # The code below is called if there is an error in the balance between credit and debit sum.
                if float_compare(credit_sum, debit_sum, precision_digits=precision) == -1:
                    self.adjust_differenced_amount(credit_sum, debit_sum, line_ids)
                elif float_compare(debit_sum, credit_sum, precision_digits=precision) == -1:
                    self.adjust_differenced_amount(debit_sum, credit_sum, line_ids)

                # Add accounting lines in the move (consolidated entry)
                if self.payslip_run_id and self.payslip_run_id.group_by_analytic_account:
                    analytic_account = self.mapped('employee_id.analytic_account_id')
                    analytic_account_list = []
                    without_analytic_account_list = []
                    line_id_debit = 0
                    line_id_credit = 0
                    for line_id in line_ids:
                        line_id_debit += line_id['debit']
                        line_id_credit += line_id['credit']
                        if line_id['analytic_account_id']:
                            analytic_account_list.append(line_id)
                        else:
                            without_analytic_account_list.append(line_id)
                    move_final_list = []
                    if analytic_account:
                        for account in analytic_account:
                            account_list = []
                            move_list = []
                            for ls in analytic_account_list:
                                if ls['analytic_account_id'] == account.id:
                                    if ls['account_id'] in account_list:
                                        for vals in move_list:
                                            if ls['account_id'] == vals['account_id']:
                                                vals['debit'] += ls['debit']
                                                vals['credit'] += ls['credit']

                                    if ls['account_id'] not in account_list:
                                        account_list.append(ls['account_id'])
                                        move_list.append(ls)
                            for lis in move_list:
                                move_final_list.append(lis)
                    for acc in without_analytic_account_list:
                        move_final_list.append(acc)

                    rec_debit = 0
                    rec_credit = 0
                    for rec in move_final_list:
                        rec_debit += rec['debit']
                        rec_credit += rec['credit']

                    # The code below is called if there is an error in the balance between credit and debit sum.
                    if float_compare(rec_credit, rec_debit, precision_digits=precision) == -1:
                        self.adjust_differenced_amount(rec_credit, rec_debit, move_final_list)
                    elif float_compare(rec_debit, rec_credit, precision_digits=precision) == -1:
                        self.adjust_differenced_amount(rec_debit, rec_credit, move_final_list)

                    move_dict['line_ids'] = [(0, 0, line_vals) for line_vals in move_final_list]
                    move = self.env['account.move'].sudo().create(move_dict)
                else:
                    move_dict['line_ids'] = [(0, 0, line_vals) for line_vals in line_ids]
                    move = self.env['account.move'].sudo().create(move_dict)
                for slip in slip_mapped_data[journal_id][slip_date]:
                    slip.write({'move_id': move.id, 'date': date})
        return True

    def adjust_differenced_amount(self, number1, number2, line_ids):
        adjustment_number = number1 - number2
        for dct in line_ids:
            if dct.get('credit') > 0:
                dct.update({
                    'credit': dct['credit'] + (adjustment_number)
                    })
                break

    def action_payslip_cancel(self):
        res = super().action_payslip_cancel()
        moves = self.mapped('move_ids')
        moves.filtered(lambda x: x.state == 'posted').button_cancel()
        moves.unlink()
        return res


class AccountMove(models.Model):
    _inherit = 'account.move'

    payslip_id = fields.Many2one('hr.payslip', 'Payslip')
    payslip_employee_id = fields.Many2one('hr.employee', string='Payslip Employee')
