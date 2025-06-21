from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ExamResult(models.Model):
    _name = 'exam.result'
    _description = 'Exam Result'
    _inherit = ['mail.thread'] 

    name = fields.Char(string="Result Name", required=True)
    result_code = fields.Char(string="Result Code", required=True, default=lambda self: self.env['ir.sequence'].next_by_code('exam.result'))
    schedule_id = fields.Many2one('exam.schedule', string="Exam Name", required=True)
    class_id = fields.Many2one(related="schedule_id.class_id", store=True, string="Class", readonly=True)
    student_ids = fields.Many2one('student.student', string="Student")
    subject = fields.Char(related="schedule_id.subject", store=True, string="Subject", readonly=True)
    exam_date = fields.Date(related="schedule_id.date", store=True, string="Exam Date", readonly=True)
    total_marks = fields.Float(related="schedule_id.total_marks", string="Total Marks", readonly=True)
    passing_marks = fields.Float(related="schedule_id.passing_marks", string="Passing Marks", readonly=True)
    grading_scale = fields.Selection(related="schedule_id.grading_scale", string="Grading Scale", readonly=True)
    is_practical = fields.Boolean(related="schedule_id.is_practical", string="Is Practical Exam?", readonly=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('published', 'Published'),
    ], string="Status", default='draft')
    remarks = fields.Text(string="Remarks")
    student_addline = fields.One2many('student.result','student_unique',string="Student result")

    @api.depends('schedule_id.student_ids')
    def _compute_total_passed(self):
        for record in self:
            record.total_passed = len([student for student in record.schedule_id.student_ids if student.total_marks >= record.passing_marks])

    @api.depends('schedule_id.student_ids')
    def _compute_total_failed(self):
        for record in self:
            record.total_failed = len([student for student in record.schedule_id.student_ids if student.total_marks < record.passing_marks])

    def action_confirm(self):
        self.write({'status': 'confirmed'})

    def action_publish(self):
        self.write({'status': 'published'})


class StudentResult(models.Model):
    _name = 'student.result'
    _description = 'Student result'


    student_unique = fields.Many2one('exam.result' ,required=True)
    student_name = fields.Many2one('student.student')
    marks_gained = fields.Float(string="Marks Gained", store=True)


