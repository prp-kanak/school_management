from odoo import fields, models, api

class TeacherTeacher(models.Model):
    _name = "teacher.teacher"
    _description = "Faculty of school"
    _inherit = ['mail.thread', 'mail.activity.mixin','mixin.model']

    # name = fields.Char(string="Name", required=True)
    profile_picture = fields.Image(string="Profile Picture", max_width=128, max_height=128)
    address = fields.Text(string="Address")
    age = fields.Integer(string="Age")
    salary = fields.Float(string="Base Salary", required=True)
    bonus = fields.Float(string="Bonus", default=0.0)
    total_salary = fields.Float(string="Total Salary", compute="_compute_total_salary", store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    hire_date = fields.Date(string="Hire Date")
    qualifications = fields.Text(string="Qualifications")
    subject_specialization = fields.Char(string="Subject Specialization")
    stage = fields.Selection(
        [
            ('active', 'Active'),
            ('in_active', 'In Active'),
            ('retired', 'Retired'),
        ],
        string="Stage",
        default='active',
    )
    # student_ids = fields.One2many('student.student', 'teacher_id', string="Assigned Students")    
    class_record_ids = fields.One2many('school.class.record', 'teacher_id', string="Class Records")
    notes = fields.Text(string="Additional Notes")
    supervised_exam_count = fields.Integer(
        string="Supervised Exam Count",
        compute="_compute_supervised_exam_count",
    )
    active = fields.Boolean(string="Active", default=True)
    assigned_class = fields.Many2one('school.standard', string="Assigned Class")
    student_ids = fields.One2many('teacher.student.line', 'teacher_unique', string="Assigned Students")
    resume = fields.Binary(string="Resume", attachment=True)  # Binary field for storing file
    resume_filename = fields.Char(string="Resume Filename")  # Optional: store file name

    @api.depends('salary', 'bonus')
    def _compute_total_salary(self):
        for record in self:
            record.total_salary = record.salary + record.bonus

    def set_active(self):
        self.write({'stage': 'active'})
        return self._refresh_view()


    def set_inactive(self):
        self.write({'stage': 'in_active'})
        return self._refresh_view()

    def set_retired(self):
        for record in self:
            record.write({'stage': 'retired'})
        return self._refresh_view()

    def _refresh_view(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    # def action_search_active_teachers(self):
    #     """Search for teachers who are active."""
    #     active_teachers = self.env['teacher.teacher'].search([('stage', '=', 'active')])
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Active Teachers',
    #         'res_model': 'teacher.teacher',
    #         'view_mode': 'list,form',
    #         'domain': [('id', 'in', active_teachers.ids)],  # Show only active teachers
    #         'target': 'current',
    #     }

    # def action_browse_teacher(self):
    #     """Browse the current teacher."""
    #     teacher_to_browse = self.env['teacher.teacher'].browse(self.id)
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Teacher Details',
    #         'res_model': 'teacher.teacher',
    #         'view_mode': 'form',
    #         'res_id': teacher_to_browse.id,  # Open the specific teacher form
    #         'target': 'current',
    #     }

    def action_count_active_teachers(self):
        active_teachers_count = self.env['teacher.teacher'].search_count([('stage', '=', 'active')])
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Active Teachers Count',
                'message': f'There are {active_teachers_count} active teachers.',
                'sticky': False,
            },
    }

    def action_search_students_for_teacher(self):
        """Search for students assigned to the current teacher."""
        students = self.env['student.student'].search([('teacher_id', '=', self.id)])
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students Assigned to Teacher',
            'res_model': 'student.student',
            'view_mode': 'list,form',
            'domain': [('id', 'in', students.ids)],  # Show students assigned to this teacher
            'target': 'current',
        }

    
    def _compute_supervised_exam_count(self):
        """Compute the count of exams supervised by the teacher."""
        for teacher in self:
            teacher.supervised_exam_count = self.env['exam.schedule'].search_count(
                [('supervisor_id', '=', teacher.id)]
            )

    def action_open_supervised_exams(self):
        self.ensure_one()
        return {
            'name': 'Scheduled Exams',
            'type': 'ir.actions.act_window',
            'res_model': 'exam.schedule',
            'view_mode': 'list,form',
            'domain': [('supervisor_id', '=', self.id)],
            'context': dict(self._context, default_supervisor_id=self.id),
        }

    @api.onchange('assigned_class')
    def _onchange_assigned_class(self):
            for record in self:
                if record.assigned_class:
                    students = self.env['student.student'].search([('class_id', '=', record.assigned_class.id)])
                    record.student_ids = [(5, 0, 0)] 
                    record.student_ids = [(0, 0, {'students_name': student.id}) for student in students]
                else:
                    record.student_ids = [(5, 0, 0)]

class TeacherStudentLine(models.Model):
    _name = "teacher.student.line"
    _description = "Teacher Student Line"

    teacher_unique = fields.Many2one('teacher.teacher',required=True, ondelete="cascade")
    students_name = fields.Many2one('student.student',required=True)
    





