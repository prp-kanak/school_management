from odoo import models, fields, api

class StudentAttendance(models.Model):
    _name = 'student.attendance'
    _description = 'Student Attendance'

    student_id = fields.Many2one('student.student', string="Student", required=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    status = fields.Selection(
        [('present', 'Present'), ('absent', 'Absent')],
        string="Status",
        required=True,
        default='present'
    )
    remarks = fields.Text(string="Remarks")

    @api.model_create_multi
    def create(self, vals):
        res = super(StudentAttendance, self).create(vals)
        res.write({'remarks': f"Attendance record created for {res.student_id.name} on {res.date}."})
        return res


    # def write(self, vals):
    #     print("Updating record with vals:", vals)
    #     res = super(StudentAttendance, self).write(vals)#update a record

    #     if 'status' in vals:
    #         print("Creating a new record due to status update")
    #         new_record_vals = {
    #             'student_id': self.student_id.id,
    #             'date': fields.Date.context_today(self),
    #             'status': vals.get('status', self.status),
    #             'remarks': f"New record created due to status update for {self.student_id.name}.",
    #         }
    #         self.env['student.attendance'].create(new_record_vals)
    #     return res


