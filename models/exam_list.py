from odoo import models, fields, api

class ExamList(models.Model):
    _name = 'exam.exam'
    _description = 'Exam List'

    name = fields.Char(string="Exam Name")
    exam_code = fields.Char(string="Exam Code")
    exam_date = fields.Date(string="Exam Date")
    start_time = fields.Float(string="Start Time (24hr format)")
    end_time = fields.Float(string="End Time (24hr format)")
    class_id = fields.Many2one('school.standard', string="Class")
    subject = fields.Char(string="Subject")
    total_marks = fields.Float(string="Total Marks")
    passing_marks = fields.Float(string="Passing Marks")
    grading_scale = fields.Selection(
        [('a', 'A-F'), ('percentage', 'Percentage'), ('points', 'Points')],
        string="Grading Scale",
        default='percentage',
      
    )
    supervisor_id = fields.Many2one('teacher.teacher', string="Supervisor")
    supervisor_contact = fields.Char(string="Supervisor Contact", readonly=True)
    remarks = fields.Text(string="Remarks")
    is_retake_allowed = fields.Boolean(string="Allow Retake?")
    late_policy = fields.Text(string="Late Policy")
    student_id = fields.Many2one(
        'student.student', string='Student', ondelete='cascade'
    )
    marks_obtained = fields.Float(string='Marks Obtained')

    @api.onchange('supervisor_id')
    def _onchange_supervisor(self):
        if self.supervisor_id:
            self.supervisor_contact = self.supervisor_id.phone

    @api.model_create_multi
    def create(self, vals):
        if vals.get('total_marks') < vals.get('passing_marks'):
            raise ValidationError("Total Marks cannot be less than Passing Marks.")
        return super(ExamList, self).create(vals)
