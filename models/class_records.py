from odoo import models, fields, api

class SchoolClassRecord(models.Model):
    _name = 'school.class.record'
    _description = 'Class Records'

    class_id = fields.Many2one('school.standard', string="Class", required=True)
    date = fields.Date(string="Date", required=True)
    attendance = fields.Integer(string="Attendance")
    notes = fields.Text(string="Notes")
    student_ids = fields.One2many(
        'student.student.line',  
        'class_record_id',  # Reverse relationship field in the student line model
        string="Students",
        help="Students associated with this class record."
    )
    teacher_id = fields.Many2one(
        'teacher.teacher',
        string="Teacher",
        help="Teacher responsible for this class on the specified date."
    )
    total_students = fields.Integer(
        string="Total Students",
        compute="_compute_total_students",
        store=True
    )

    @api.depends('student_ids')
    def _compute_total_students(self):
        for record in self:
            record.total_students = len(record.student_ids)

    @api.onchange('class_id')
    def _onchange_class_id(self):
        for record in self:
            if record.class_id:
                students = self.env['student.student'].search([('class_id', '=', record.class_id.id)])
                record.student_ids = [(5, 0, 0)]  
                record.student_ids = [
                    (0, 0, {'student_id': student.id, 'student_name': student.name})
                    for student in students
                ]
            else:
                record.student_ids = [(5, 0, 0)] 

class StudentStudentLine(models.Model):
    _name = 'student.student.line'
    _description = 'Student Line'

    class_record_id = fields.Many2one('school.class.record', string="Class Record", ondelete="cascade")
    student_id = fields.Many2one('student.student', string="Student", required=True)
    student_name = fields.Char(string="Student Name", related="student_id.name")
