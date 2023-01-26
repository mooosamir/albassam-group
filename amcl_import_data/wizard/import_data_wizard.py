import binascii
import tempfile
import datetime

import xlrd
from odoo.exceptions import ValidationError
from odoo import fields, models


class ImportData(models.TransientModel):
    _name = 'amcl.import.data'
    _description = 'Import Data'

    import_file = fields.Binary(string='File')


    def action_to_import(self):
        if not self.import_file:
            raise ValidationError("There is no file to import.")
        employee_obj = self.env["hr.employee"]
        company_obj = self.env["res.company"]
        department_obj = self.env["hr.department"]

        fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.import_file))
        fp.seek(0)
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(3)

        if self.import_file:
            for row_no in range(sheet.nrows):
                vals = {}
                if row_no <= 0:
                    map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
                else:
                    line = sheet.row_values(row_no)

                    if hasattr(employee_obj, 'employee_sequence'):
                        vals.update({
                            'employee_sequence': line[0]
                            })

                    if line[1]:
                        all_names = self.get_employee_name(line[1])
                        vals.update(all_names)

                    if line[2]:
                        vals.update({
                            'company_country_code': line[2]
                            })

                    if line[3]:
                        company_id = company_obj.search([('name','=', line[3])])
                        if not company_id.id:
                            raise ValidationError("Company '%s' not found."%(line[3]))
                        vals.update({
                            'company_id': company_id.id
                            })

                    # if line[4]:
                    #     vals.update({
                    #         })

                    if line[5]:
                        department_id = department_obj.search([('name','=', line[5]),('company_id.name','=',line[3])])
                        if not department_id.id:
                            raise ValidationError("Department '%s' not found."%(line[5]))
                        vals.update({
                            'department_id': department_id.id
                            })

                    # if line[6]:
                    #     religion = line[6]
                    #     vals.update({
                    #         'religion': religion
                    #         })

                    if line[7]:
                        country_id = self.env['res.country'].search([('name','=',line[7])])
                        vals.update({
                            'country_id': country_id and country_id.id
                            })

                    if line[8]:
                        job_id = self.env['hr.job'].search([('name','=',line[8]),('company_id.name','=',line[3])])
                        if not job_id.id:
                            raise ValidationError("Job Position '%s' not found."%(line[8]))
                        vals.update({
                            'job_id': job_id and job_id.id
                            })

                    # if line[9]:
                    #     class = line[9]
                    #     vals.update({
                    #         'class': class
                    #         })

                    # if line[10]:
                    #     grade = line[10]
                    #     vals.update({
                    #         'grade': grade
                    #         })

                    # if line[11]:
                    #     hiring_date = line[11]
                    #     vals.update({
                    #         'hiring_date': hiring_date
                    #         })

                    # if line[12]:
                    #     service_time = line[12]
                    #     vals.update({
                    #         'service_time': service_time
                    #         })

                    # if line[13]:
                    #     basic_salary = line[13]
                    #     vals.update({
                    #         'basic_salary': basic_salary
                    #         })

                    # if line[14]:
                    #     total_salary = line[14]
                    #     vals.update({
                    #         'total_salary: total_salary
                    #         })

                    if line[15]:
                        if isinstance(line[15], str):
                            birthday = datetime.datetime.strptime(line[15], '%d/%m/%Y')
                        else:
                            birthday = datetime.datetime(*xlrd.xldate_as_tuple(line[15], workbook.datemode))
                        vals.update({
                            'birthday': birthday
                            })

                    # if line[16]:
                    #     age = line[16]
                    #     vals.update({
                    #         'age: age
                    #         })

                    # if line[17]:
                    #     health_ins = line[17]
                    #     vals.update({
                    #         'health_ins: health_ins
                    #         })

                    # if line[18]:
                    #     health_ins_date = line[18]
                    #     vals.update({
                    #         'health_ins_date: health_ins_date
                    #         })

                    # if line[19]:
                    #     contarct_type = line[19]
                    #     vals.update({
                    #         'contarct_type: contarct_type
                    #         })

                    # if line[20]:
                    #     employment_date = line[20]
                    #     vals.update({
                    #         'employment_date: employment_date
                    #         })

                    # if line[21]:
                    #     service_time = line[21]
                    #     vals.update({
                    #         'service_time: service_time
                    #         })
                    employee_obj.sudo().create(vals)

    def get_employee_name(self, emp_name):
        split_name = emp_name.split(' ')
        all_names = {}
        if len(split_name) == 1:
            all_names.update({
                'name': split_name[0]
                })
        elif len(split_name) == 2:
            all_names.update({
                'name': split_name[0],
                'last_name': split_name[1]
                })
        elif len(split_name) == 3:
            all_names.update({
                'name': split_name[0],
                'middle_name': split_name[1],
                'last_name': split_name[2]
                })
        elif len(split_name) == 4:
            all_names.update({
                'name': split_name[0],
                'middle_name': split_name[1],
                'grand_father_name': split_name[2],
                'last_name': split_name[3]
                })
        elif len(split_name) >= 4:
            all_names.update({
                'name': split_name[0],
                'middle_name': split_name[1],
                'grand_father_name': split_name[2],
                'last_name': ' '.join(split_name[3:])
                })
        return all_names