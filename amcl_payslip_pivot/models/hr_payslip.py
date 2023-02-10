# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import models, fields, api
from odoo import tools
from psycopg2 import sql


class HrPayrollCustomReport(models.Model):
    _name = "hr.payroll.custom.report"
    _description = "Payroll Analysis Report"
    _auto = False
    _rec_name = 'date_from'
    _order = 'date_from desc'


    count = fields.Integer('# Payslip', group_operator="sum", readonly=True)
    count_work = fields.Integer('Work Days', group_operator="sum", readonly=True)
    count_work_hours = fields.Integer('Work Hours', group_operator="sum", readonly=True)
    count_leave = fields.Integer('Days of Paid Time Off', group_operator="sum", readonly=True)
    count_leave_unpaid = fields.Integer('Days of Unpaid Time Off', group_operator="sum", readonly=True)
    count_unforeseen_absence = fields.Integer('Days of Unforeseen Absence', group_operator="sum", readonly=True)

    name = fields.Char('Payslip Name', readonly=True)
    payslip_number = fields.Char(string='Payslip Number', readonly=True)
    date_from = fields.Date('Start Date', readonly=True)
    date_to = fields.Date('End Date', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)

    employee_id = fields.Many2one('hr.employee', 'Employee', readonly=True)
    employee_code = fields.Char(string='Employee Code')
    department_id = fields.Many2one('hr.department', 'Department', readonly=True)
    job_id = fields.Many2one('hr.job', 'Job Position', readonly=True)
    number_of_days = fields.Float('Number of Days', readonly=True)
    number_of_hours = fields.Float('Number of Hours', readonly=True)
    net_wage = fields.Float('Net Salary', readonly=True)
    basic_wage = fields.Float('Basic Salary', readonly=True)
    gross_wage = fields.Float('Gross Wage', readonly=True)
    transport_wage = fields.Float(string='Tansport Allowance', readonly=True)
    hra_wage = fields.Float(string='Housing Allowance', readonly=True)
    other_wage = fields.Float(string='Other Allowance', readonly=True)
    wovertime_input_wage = fields.Float(string='Input WOT')
    wovertime_wage = fields.Float(string='Worker Overtime', readonly=True)
    eovertime_wage = fields.Float(string='Employee Overtime', readonly=True)
    loan = fields.Float(string='Loan', readonly=True)
    loan_deduction = fields.Float(string='Loan Deduction', readonly=True)
    leave_basic_wage = fields.Float('Basic Wage for Time Off', readonly=True)
    gosise = fields.Float(string='GOSI Contribution for Saudi Employee', readonly=True)
    gosiccnse = fields.Float(string='GOSI Company Contrib. Non Saudi Emp', readonly=True)
    gosiccse = fields.Float(string='GOSI Company Contrib. for Saudi Emp', readonly=True)
    mobile_allow = fields.Float(string='Mobile Allowance', readonly=True)
    ticket_allow = fields.Float(string='Ticket Allowance', readonly=True)
    leave_deduction = fields.Float(string='Leave Deduction', readonly=True)
    late_deduction = fields.Float(string='Late Deduction', readonly=True)
    bonus = fields.Float(string='Bonus', readonly=True, default=0.0)
    early_go = fields.Float(string='Early Going', readonly=True)
    signon_bonus = fields.Float(string='Employee Signon Bonus', readonly=True)
    reimbursement = fields.Float(string='Employee Reimbursement', readonly=True)
    exp_deduct = fields.Float(string='Expense Deduction', readonly=True)
    emp_exp_deduct = fields.Float(string='Employee Expense Deduction', readonly=True)
    deductions = fields.Float(string='Deductions', readonly=True)
    other_deductions = fields.Float(string='Other Deductions', readonly=True)
    attach_salary = fields.Float(string='Attachment of Salary', readonly=True)
    assign_salary = fields.Float(string='Assignment of Salary', readonly=True)
    child_support = fields.Float(string='Child Support', readonly=True)
    remote_allow = fields.Float(string='Remote Allowance', readonly=True)

    #====================== Additional Fields ==================
    food_allowance = fields.Float(string='Food Allowance', readonly=True)
    internet_allowance = fields.Float(string='Internet Allowance', readonly=True)
    lab_allowance = fields.Float(string='LAB Allowance', readonly=True)
    mfl_allowance = fields.Float(string='MFL/Guided Wava/Tube Allowance', readonly=True)
    rpp_allowance = fields.Float(string='RPP Allowance', readonly=True)
    sen_allowance = fields.Float(string='Seniority Allowance', readonly=True)
    sup_allowance = fields.Float(string='Supervisory Allowance', readonly=True)
    ut_ut_allowance = fields.Float(string='UT/UT Shear Allowance', readonly=True)
    rtfi_allowance = fields.Float(string='RTFI Allowance', readonly=True)
    rso_allowance = fields.Float(string='RSO Allowance', readonly=True)
    add_allowance = fields.Float(string='Additional Tasks Allowance', readonly=True)
    other_income = fields.Float(string='Other Income', readonly=True)

    work_code = fields.Many2one('hr.work.entry.type', 'Work type', readonly=True)
    work_type = fields.Selection([
        ('1', 'Regular Working Day'),
        ('2', 'Paid Time Off'),
        ('3', 'Unpaid Time Off')], string='Work, (un)paid Time Off', readonly=True)

    def _select(self):
        return """
            SELECT
                p.id as id,
                CASE WHEN wd.id = min_id.min_line THEN 1 ELSE 0 END as count,
                -- CASE WHEN wet.is_leave THEN 0 ELSE wd.number_of_days END as count_work,
                p.month_days as count_work,
                -- CASE WHEN wet.is_leave THEN CASE WHEN wd.number_of_days is not null THEN wd.number_of_days ELSE 0 END ELSE 0 END as count_work,
                CASE WHEN wet.is_leave THEN 0 ELSE wd.number_of_hours END as count_work_hours,
                CASE WHEN wet.is_leave and wd.amount <> 0 THEN wd.number_of_days ELSE 0 END as count_leave,
                CASE WHEN wet.is_leave and wd.amount = 0 THEN wd.number_of_days ELSE 0 END as count_leave_unpaid,
                CASE WHEN wet.is_unforeseen THEN wd.number_of_days ELSE 0 END as count_unforeseen_absence,
                CASE WHEN wet.is_leave THEN wd.amount ELSE 0 END as leave_basic_wage,
                p.name as name,
                p.number as payslip_number,
                p.date_from as date_from,
                p.date_to as date_to,
                e.id as employee_id,
                e.employee_code as employee_code,
                e.department_id as department_id,
                c.job_id as job_id,
                e.company_id as company_id,
                wet.id as work_code,
                CASE WHEN wet.is_leave IS NOT TRUE THEN '1' WHEN wd.amount = 0 THEN '3' ELSE '2' END as work_type,
                wd.number_of_days as number_of_days,
                wd.number_of_hours as number_of_hours,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pln.total is not null THEN pln.total ELSE 0 END ELSE 0 END as net_wage,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN plb.total is not null THEN plb.total ELSE 0 END ELSE 0 END basic_wage,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN plg.total is not null THEN plg.total ELSE 0 END ELSE 0 END as gross_wage,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_transport.total is not null THEN pl_transport.total ELSE 0 END ELSE 0 END as transport_wage,
                -- CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_other.total is not null THEN pl_other.total ELSE 0 END ELSE 0 END as other_wage,
                -- CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_wovertime_input.total is not null THEN pl_wovertime_input.total ELSE 0 END ELSE 0 END as wovertime_input_wage,
                -- CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_wovertime.total is not null THEN pl_wovertime.total ELSE 0 END ELSE 0 END as wovertime_wage,
                -- CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_eovertime.total is not null THEN pl_eovertime.total ELSE 0 END ELSE 0 END as eovertime_wage,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_loan.total is not null THEN pl_loan.total ELSE 0 END ELSE 0 END as loan,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_loan_deduction.total is not null THEN pl_loan_deduction.total ELSE 0 END ELSE 0 END as loan_deduction,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_gosise.total is not null THEN pl_gosise.total ELSE 0 END ELSE 0 END as gosise,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_gosiccnse.total is not null THEN pl_gosiccnse.total ELSE 0 END ELSE 0 END as gosiccnse,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_gosiccse.total is not null THEN pl_gosiccse.total ELSE 0 END ELSE 0 END as gosiccse,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_mobile.total is not null THEN pl_mobile.total ELSE 0 END ELSE 0 END as mobile_allow,
                -- CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_ticket.total is not null THEN pl_ticket.total ELSE 0 END ELSE 0 END as ticket_allow,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_leave.total is not null THEN pl_leave.total ELSE 0 END ELSE 0 END as leave_deduction,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_late.total is not null THEN pl_late.total ELSE 0 END ELSE 0 END as late_deduction,
                -- CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_bonus.total is not null THEN pl_bonus.total ELSE 0 END ELSE 0 END as bonus,
                -- CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_earlygo.total is not null THEN pl_earlygo.total ELSE 0 END ELSE 0 END as early_go,
                -- CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_signon.total is not null THEN pl_signon.total ELSE 0 END ELSE 0 END as signon_bonus,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_reimbursement.total is not null THEN pl_reimbursement.total ELSE 0 END ELSE 0 END as reimbursement,
                -- CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_exp_deduct.total is not null THEN pl_exp_deduct.total ELSE 0 END ELSE 0 END as exp_deduct,
                -- CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_emp_exp_deduct.total is not null THEN pl_emp_exp_deduct.total ELSE 0 END ELSE 0 END as emp_exp_deduct,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_deductions.total is not null THEN pl_deductions.total ELSE 0 END ELSE 0 END as deductions,
                -- CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_other_deductions.total is not null THEN pl_other_deductions.total ELSE 0 END ELSE 0 END as other_deductions,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_attach_salary.total is not null THEN pl_attach_salary.total ELSE 0 END ELSE 0 END as attach_salary,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_assign_salary.total is not null THEN pl_assign_salary.total ELSE 0 END ELSE 0 END as assign_salary,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_child_support.total is not null THEN pl_child_support.total ELSE 0 END ELSE 0 END as child_support,
                -- CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_remote_allow.total is not null THEN pl_remote_allow.total ELSE 0 END ELSE 0 END as remote_allow,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_hra.total is not null THEN pl_hra.total ELSE 0 END ELSE 0 END as hra_wage,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_food_allowance.total is not null THEN pl_food_allowance.total ELSE 0 END ELSE 0 END as food_allowance,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_internet_allowance.total is not null THEN pl_internet_allowance.total ELSE 0 END ELSE 0 END as internet_allowance,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_lab_allowance.total is not null THEN pl_lab_allowance.total ELSE 0 END ELSE 0 END as lab_allowance,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_mfl_allowance.total is not null THEN pl_mfl_allowance.total ELSE 0 END ELSE 0 END as mfl_allowance,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_rpp_allowance.total is not null THEN pl_rpp_allowance.total ELSE 0 END ELSE 0 END as rpp_allowance,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_sen_allowance.total is not null THEN pl_sen_allowance.total ELSE 0 END ELSE 0 END as sen_allowance,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_sup_allowance.total is not null THEN pl_sup_allowance.total ELSE 0 END ELSE 0 END as sup_allowance,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_ut_ut_allowance.total is not null THEN pl_ut_ut_allowance.total ELSE 0 END ELSE 0 END as ut_ut_allowance,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_rtfi_allowance.total is not null THEN pl_rtfi_allowance.total ELSE 0 END ELSE 0 END as rtfi_allowance,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_rso_allowance.total is not null THEN pl_rso_allowance.total ELSE 0 END ELSE 0 END as rso_allowance,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_add_allowance.total is not null THEN pl_add_allowance.total ELSE 0 END ELSE 0 END as add_allowance,
                CASE WHEN wd.id = min_id.min_line THEN CASE WHEN pl_other_income.total is not null THEN pl_other_income.total ELSE 0 END ELSE 0 END as other_income"""


    def _from(self, where_date_clause='', where_company_clause=''):
        return """FROM
            (SELECT * FROM hr_payslip WHERE state IN ('done', 'paid', 'verify') %s %s ) p
                left join hr_employee e on (p.employee_id = e.id)
                left join hr_payslip_worked_days wd on (wd.payslip_id = p.id)
                left join hr_work_entry_type wet on (wet.id = wd.work_entry_type_id)
                left join (select payslip_id, min(id) as min_line from hr_payslip_worked_days group by payslip_id) min_id on (min_id.payslip_id = p.id)
                left join hr_payslip_line pln on (pln.slip_id = p.id and pln.code = 'NET')
                left join hr_payslip_line plb on (plb.slip_id = p.id and plb.code = 'BASIC')
                left join hr_payslip_line plg on (plg.slip_id = p.id and plg.code = 'GROSS')
                left join hr_payslip_line pl_hra on (pl_hra.slip_id = p.id and pl_hra.code = 'HRA')
                -- left join hr_payslip_line pl_other on (pl_other.slip_id = p.id and pl_other.code = 'Other Allowance')
                -- left join hr_payslip_line pl_wovertime_input on (pl_wovertime_input.slip_id = p.id and pl_wovertime_input.code = 'overtime')
                -- left join hr_payslip_line pl_wovertime on (pl_wovertime.slip_id = p.id and pl_wovertime.code = 'Overtime')
                -- left join hr_payslip_line pl_eovertime on (pl_eovertime.slip_id = p.id and pl_eovertime.code = 'OVERTIME')
                left join hr_payslip_line pl_transport on (pl_transport.slip_id = p.id and pl_transport.code = 'TA')
                left join hr_payslip_line pl_gosise on (pl_gosise.slip_id = p.id and pl_gosise.code = 'GOSI-S-E')
                left join hr_payslip_line pl_gosiccnse on (pl_gosiccnse.slip_id = p.id and pl_gosiccnse.code = 'GOSI-Company-Contribution-Non-Saudi-Employee')
                left join hr_payslip_line pl_gosiccse on (pl_gosiccse.slip_id = p.id and pl_gosiccse.code = 'GOSI-Company-Contribution-Saudi-Employee')
                left join hr_payslip_line pl_loan on (pl_loan.slip_id = p.id and pl_loan.code = 'LOAN')
                left join hr_payslip_line pl_loan_deduction on (pl_loan_deduction.slip_id = p.id and pl_loan_deduction.code = 'LOANDEDUCTION')
                left join hr_payslip_line pl_mobile on (pl_mobile.slip_id = p.id and pl_mobile.code = 'MOB')
                -- left join hr_payslip_line pl_ticket on (pl_ticket.slip_id = p.id and pl_ticket.code = 'TICKET')
                left join hr_payslip_line pl_leave on (pl_leave.slip_id = p.id and pl_leave.code = 'Unpaid Leave')
                left join hr_payslip_line pl_late on (pl_late.slip_id = p.id and pl_late.code = 'LATE')
                -- left join hr_payslip_line pl_bonus on (pl_bonus.slip_id = p.id and pl_bonus.code = 'BONUS')
                -- left join hr_payslip_line pl_earlygo on (pl_earlygo.slip_id = p.id and pl_earlygo.code = 'EARLYGO')
                -- left join hr_payslip_line pl_signon on (pl_signon.slip_id = p.id and pl_signon.code = 'SIGNON')
                left join hr_payslip_line pl_reimbursement on (pl_reimbursement.slip_id = p.id and pl_reimbursement.code = 'REIMBURSEMENT')
                -- left join hr_payslip_line pl_exp_deduct on (pl_exp_deduct.slip_id = p.id and pl_exp_deduct.code = 'Expense')
                -- left join hr_payslip_line pl_emp_exp_deduct on (pl_emp_exp_deduct.slip_id = p.id and pl_emp_exp_deduct.code = 'Employee-Expense-Deduction')
                left join hr_payslip_line pl_deductions on (pl_deductions.slip_id = p.id and pl_deductions.code = 'DEDUCTION')
                -- left join hr_payslip_line pl_other_deductions on (pl_other_deductions.slip_id = p.id and pl_other_deductions.code = 'OTHER_DEDUCTION')
                left join hr_payslip_line pl_attach_salary on (pl_attach_salary.slip_id = p.id and pl_attach_salary.code = 'ATTACH_SALARY')
                left join hr_payslip_line pl_assign_salary on (pl_assign_salary.slip_id = p.id and pl_assign_salary.code = 'ASSIG_SALARY')
                left join hr_payslip_line pl_child_support on (pl_child_support.slip_id = p.id and pl_child_support.code = 'CHILD_SUPPORT')
                -- left join hr_payslip_line pl_remote_allow on (pl_remote_allow.slip_id = p.id and pl_remote_allow.code = 'Remote-Allowance')
                left join hr_payslip_line pl_food_allowance on (pl_food_allowance.slip_id = p.id and pl_food_allowance.code = 'FOD')
                left join hr_payslip_line pl_internet_allowance on (pl_internet_allowance.slip_id = p.id and pl_internet_allowance.code = 'INT')
                left join hr_payslip_line pl_lab_allowance on (pl_lab_allowance.slip_id = p.id and pl_lab_allowance.code = 'LAB')
                left join hr_payslip_line pl_mfl_allowance on (pl_mfl_allowance.slip_id = p.id and pl_mfl_allowance.code = 'MFL')
                left join hr_payslip_line pl_rpp_allowance on (pl_rpp_allowance.slip_id = p.id and pl_rpp_allowance.code = 'RPP')
                left join hr_payslip_line pl_sen_allowance on (pl_sen_allowance.slip_id = p.id and pl_sen_allowance.code = 'SEN')
                left join hr_payslip_line pl_sup_allowance on (pl_sup_allowance.slip_id = p.id and pl_sup_allowance.code = 'SUP')
                left join hr_payslip_line pl_ut_ut_allowance on (pl_ut_ut_allowance.slip_id = p.id and pl_ut_ut_allowance.code = 'UT/UT')
                left join hr_payslip_line pl_rtfi_allowance on (pl_rtfi_allowance.slip_id = p.id and pl_rtfi_allowance.code = 'RTFI')
                left join hr_payslip_line pl_rso_allowance on (pl_rso_allowance.slip_id = p.id and pl_rso_allowance.code = 'RSO')
                left join hr_payslip_line pl_add_allowance on (pl_add_allowance.slip_id = p.id and pl_add_allowance.code = 'ADD')
                left join hr_payslip_line pl_other_income on (pl_other_income.slip_id = p.id and pl_other_income.code = 'Other_Income')
                left join hr_contract c on (p.contract_id = c.id)"""%(where_date_clause, where_company_clause)

    def _group_by(self):
        return """GROUP BY
            e.id,
            e.department_id,
            e.company_id,
            wd.id,
            wet.id,
            p.id,
            p.name,
            p.number,
            p.date_from,
            p.date_to,
            pln.total,
            plb.total,
            plg.total,
            pl_hra.total,
            -- pl_other.total,
            pl_transport.total,
            -- pl_wovertime_input.total,
            -- pl_wovertime.total,
            -- pl_eovertime.total,
            pl_loan.total,
            pl_loan_deduction.total,
            pl_gosise.total,
            pl_gosiccnse.total,
            pl_gosiccse.total,
            min_id.min_line,
            pl_mobile.total,
            -- pl_ticket.total,
            pl_leave.total,
            pl_late.total,
            -- pl_bonus.total,
            -- pl_earlygo.total,
            -- pl_signon.total,
            pl_reimbursement.total,
            -- pl_exp_deduct.total,
            -- pl_emp_exp_deduct.total,
            pl_deductions.total,
            -- pl_other_deductions.total,
            pl_attach_salary.total,
            pl_assign_salary.total,
            pl_child_support.total,
            -- pl_remote_allow.total,
            pl_food_allowance.total,
            pl_internet_allowance.total,
            pl_lab_allowance.total,
            pl_mfl_allowance.total,
            pl_rpp_allowance.total,
            pl_sen_allowance.total,
            pl_sup_allowance.total,
            pl_ut_ut_allowance.total,
            pl_rtfi_allowance.total,
            pl_rso_allowance.total,
            pl_add_allowance.total,
            p.month_days,
            pl_other_income.total,
            c.id"""

    def init(self):
        where_date_clause = ''
        where_company_clause = ''
        if self.env.context.get('wizard_id', False):
            wizard_id = self.env['payroll.report.wizard'].browse(self._context.get('wizard_id'))
            self.set_view_priority(wizard_id)
            where_date_clause = self.get_where_date_clause(wizard_id)
            where_company_clause = self.get_where_company_clause(wizard_id)

        query = """
            %s
            %s
            %s
        """%(
            self._select(),
            self._from(where_date_clause, where_company_clause),
            self._group_by()
        )

        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            sql.SQL("CREATE or REPLACE VIEW {} as ({})").format(
                sql.Identifier(self._table),
                sql.SQL(query)))

    def get_where_date_clause(self, wizard_id):
        where_date_clause = ''
        if wizard_id and wizard_id.start_date and wizard_id.end_date:
            where_date_clause = "AND date_from >= '%s' AND date_to <= '%s'"%(wizard_id.start_date,wizard_id.end_date)
        return where_date_clause

    def get_where_company_clause(self, wizard_id):
        where_company_clause = ''
        if wizard_id and wizard_id.company_ids:
            if len(wizard_id.company_ids) == 1:
                where_company_clause += "AND company_id in (%s)"%(wizard_id.company_ids.id)
            elif len(wizard_id.company_ids) > 1:
                where_company_clause += "AND company_id in %s"%(str(wizard_id.company_ids._ids))
        return where_company_clause

    def set_view_priority(self, wizard_id):
        # One Pivot view will be priotised based on company code to show the detail in browser
        # If no company or more than one company is selected then 'general_view' will be priotised
        all_pivot_view_ids = self.get_all_pivot_views()
        act_window_id = all_pivot_view_ids.get('general_view')
        if len(wizard_id.company_ids) == 1:
            act_window_id = all_pivot_view_ids.get(wizard_id.company_ids.company_code, 'general_view')
        act_window_id.write({
            'priority': 10
        })
        for each in all_pivot_view_ids:
            if all_pivot_view_ids[each] != act_window_id:
                all_pivot_view_ids[each].write({
                    'priority': 99
                    })

    def get_all_pivot_views(self):
        # Dictionary of all the existing pivot view of this model
        all_pivot_view_ids = {
            'general_view': self.env.ref('amcl_payslip_pivot.hr_payroll_custom_report_view_pivot'),
            'ISS': self.env.ref('amcl_payslip_pivot.hr_payroll_custom_report_view_pivot_ISS'),
            'GHI': self.env.ref('amcl_payslip_pivot.hr_payroll_custom_report_view_pivot_GHI'),
        }
        return all_pivot_view_ids