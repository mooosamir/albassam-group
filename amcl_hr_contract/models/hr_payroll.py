# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, models, fields, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    def action_payslip_draft(self):
        res = super(HrPayslip, self).action_payslip_draft()
        if self.move_ids:
            for line in self.move_ids:
                if line.state == 'draft':
                    line.unlink()
        return res

    @api.depends('contract_id')
    def check_signon_deduction(self):
        slip_obj = self.env['hr.payslip']
        total_amt_deduct = 0.00
        employee_id = self.contract_id.employee_id
        date_of_leave = False
        if employee_id.date_of_leave:
            date_of_leave = datetime.strptime(str(employee_id.date_of_leave), DEFAULT_SERVER_DATE_FORMAT).date()
        if date_of_leave and employee_id.date_of_leave and employee_id.duration_in_months < 13 and date_of_leave < datetime.now().date():
            for slip_id in slip_obj.search([('state', '=', 'done')]):
                for slip_line_id in slip_id.line_ids:
                    if slip_line_id.code == 'SIGNON':
                        total_amt_deduct += slip_line_id.total
        return total_amt_deduct

    @api.model
    def get_inputs(self, contract_ids, date_from, date_to):
        res = super(HrPayslip, self).get_inputs(contract_ids, date_from, date_to)
        for contract in contract_ids:
            if not contract.employee_id.date_of_leave and contract.signon_bonus_amount > 0:
                for period in contract.period_ids:
                    if len(contract.period_ids) > 0:
                        signon_amt = contract.signon_bonus_amount / len(contract.period_ids)
                    if period.date_start == self.date_from or period.date_stop == self.date_to:
                        res.append({
                            'name': 'Sign on Bonus',
                            'code': 'SIGNON_BONUS',
                            'amount': signon_amt or 0.00,
                            'contract_id': contract.id,
                        })
            signon_amount = self.check_signon_deduction()
            if signon_amount > 0:
                res.append({
                    'name': 'SIGNON Bonus Deduction',
                    'code': 'SIGNON_DEDUCTION',
                    'amount': signon_amount,
                    'contract_id': contract.id,
                })
        return res

    def _get_worked_day_lines_values(self, domain=None):
        self.ensure_one()
        res = []
        hours_per_day = self._get_worked_day_lines_hours_per_day()
        work_hours = self.contract_id._get_work_hours(self.date_from, self.date_to, domain=domain)
        work_hours_ordered = sorted(work_hours.items(), key=lambda x: x[1])
        biggest_work = work_hours_ordered[-1][0] if work_hours_ordered else 0
        add_days_rounding = 0
        for work_entry_type_id, hours in work_hours_ordered:
            work_entry_type = self.env['hr.work.entry.type'].browse(work_entry_type_id)
            days = round(hours / hours_per_day, 5) if hours_per_day else 0
            if work_entry_type_id == biggest_work:
                days += add_days_rounding

            day_rounded = self._round_days(work_entry_type, days)
            add_days_rounding += (days - day_rounded)
            if work_entry_type.name == 'Attendance':
                day_rounded = self.payment_days
                hours = day_rounded * hours_per_day
            attendance_line = {
                'sequence': work_entry_type.sequence,
                'work_entry_type_id': work_entry_type_id,
                'number_of_days': day_rounded,
                'number_of_hours': hours,
            }
            res.append(attendance_line)
        return res


class HrPayslipWorkdaysInherit(models.Model):
    _inherit = 'hr.payslip.worked_days'

    @api.depends('is_paid', 'number_of_hours', 'payslip_id', 'payslip_id.normal_wage', 'payslip_id.sum_worked_hours')
    def _compute_amount(self):
        for worked_days in self.filtered(lambda wd: not wd.payslip_id.edited):
            if not worked_days.contract_id or worked_days.code == 'OUT':
                worked_days.amount = 0
                continue
            if worked_days.payslip_id.wage_type == "hourly":
                worked_days.amount = worked_days.payslip_id.contract_id.hourly_wage * worked_days.number_of_hours if worked_days.is_paid else 0
            else:
                worked_days.amount = worked_days.payslip_id.contract_id.wage * worked_days.number_of_days / (
                        worked_days.payslip_id.payment_days + worked_days.payslip_id.leave_days or 1) if worked_days.is_paid else 0

    @api.model
    def create(self, vals):
        """Update Work Days and Hours."""
        res = super(HrPayslipWorkdaysInherit, self).create(vals)
        if res.work_entry_type_id.name == 'Attendance':
            hours_per_day = res.payslip_id._get_worked_day_lines_hours_per_day()
            res.number_of_days = res.payslip_id.payment_days
            res.number_of_hours = res.number_of_days * hours_per_day
        return res
