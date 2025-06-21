from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class ExamSchedule(models.Model):
    _name = 'exam.schedule'
    _description = 'Exam Schedule'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Exam Name")
    exam_code = fields.Char(string="Exam Code")
    date = fields.Date(string="Exam Date")
    start_time = fields.Float(string="Start Time", required=True)
    end_time = fields.Float(string="End Time", required=True)
    duration = fields.Float(string="Duration (hours)", compute='_compute_duration', store=True)
    class_id = fields.Many2one('school.standard', string="Class", required=True)
    subject = fields.Char(string="Subject", required=True)
    room_number = fields.Char(string="Room Number")
    total_marks = fields.Float(string="Total Marks", required=True)
    passing_marks = fields.Float(string="Passing Marks", required=True)
    is_practical = fields.Boolean(string="Is Practical Exam?")
    grading_scale = fields.Selection(
        [('a', 'A-F'), ('percentage', 'Percentage'), ('points', 'Points')],
        string="Grading Scale",
        default='percentage',
        required=True
    )
    supervisor_id = fields.Many2one(
        'teacher.teacher', string="Supervisor", required=True
    )
    supervisor_contact = fields.Char(string="Supervisor Contact", readonly=True)
    remarks = fields.Text(string="Remarks")
    is_retake_allowed = fields.Boolean(string="Allow Retake?")
    late_policy = fields.Text(string="Late Policy")
    student_ids = fields.Many2many('student.student', string="Students", required=True)
    syllabus_id = fields.Many2one(
        'syllabus.syllabus', 
        string='Syllabus', 
        help='Select the syllabus associated with this exam schedule'
    )
    status = fields.Selection(
        [('scheduled', 'Scheduled'),
         ('ongoing', 'Ongoing'),
         ('completed', 'Completed')],
        string="Status", default='scheduled', tracking=True
    )
    sequence_no = fields.Char(string='Sequence', required=True, copy=False, readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('school_management.exam_schedule') or 'New')
    team_head_id = fields.Many2one('res.users',string="Team Leader",tracking=True)



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence_no', 'New') == 'New':
                vals['sequence_no'] = self.env['ir.sequence'].next_by_code('exam.schedule') or 'New'
        return super(ExamSchedule, self).create(vals)


    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for record in self:
            if record.start_time and record.end_time:
                start_time = datetime.strptime(f"{int(record.start_time)}:{int((record.start_time % 1) * 60):02d}", "%H:%M")
                end_time = datetime.strptime(f"{int(record.end_time)}:{int((record.end_time % 1) * 60):02d}", "%H:%M")

                if end_time > start_time:
                    duration = end_time - start_time
                    record.duration = duration.total_seconds() / 3600  
                else:
                    record.duration = 0.0  
            else:
                record.duration = 0.0
    @api.constrains('passing_marks', 'total_marks')
    def _check_marks(self):
        for record in self:
            if record.passing_marks > record.total_marks:
                raise ValidationError("Passing marks cannot exceed total marks.")
            if record.passing_marks < 0 or record.total_marks < 0:
                raise ValidationError("Marks cannot be negative.")

    @api.onchange('supervisor_id')
    def _onchange_supervisor(self):
        if self.supervisor_id:
            self.supervisor_contact = self.supervisor_id.phone


    @api.onchange('class_id')
    def _onchange_class_id(self):
        if self.class_id:
            students = self.env['student.student'].search([('class_id', '=', self.class_id.id)])
            self.student_ids = [(6, 0, students.ids)]
        else:
            self.student_ids = [(5, 0)]


    @api.model_create_multi
    def update_exam_status(self):
        overdue_exams = self.search([('date', '<', fields.Date.today()), ('status', '!=', 'completed')])
        for exam in overdue_exams:
            exam.status = 'completed'
            exam.message_post(body=f"The status of the exam '{exam.name}' has been updated to 'Completed'.")

      
    @api.model
    def notify_upcoming_exams(self):
        today = datetime.today().date()
        next_two_days = today + timedelta(days=2)

        upcoming_exams = self.search([
            ('date', '>=', today),
            ('date', '<=', next_two_days)
        ])

        template = self.env.ref('school_management.email_template_exam_reminder', raise_if_not_found=False)

        if not template:
            raise ValueError("Email template 'email_template_exam_reminder' not found.")

        for exam in upcoming_exams:
            for student in exam.student_ids:
                if student.email:
                    template.send_mail(exam.id, email_values={'email_to': student.email}, force_send=True)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Exam Notifications Sent',
                'message': f'Emails sent for {len(upcoming_exams)} upcoming exams.',
                'type': 'success',
            },
        }