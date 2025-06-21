from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Assignment(models.Model):
    _name = 'teacher.assignment'
    _description = 'Teacher Assignment'

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    teacher_id = fields.Many2one('teacher.teacher', string="Assigned by", required=True)
    due_date = fields.Date(string="Due Date")
    class_id = fields.Many2one('school.standard', string="Class Name", required=True)
    student_ids = fields.Many2many('student.student', string="Assigned Students", 
                                   domain="[('class_id', '=', class_id)]")
    
    @api.onchange('class_id')
    def _onchange_class_id(self):
        if self.class_id:
            students = self.env['student.student'].search([('class_id', '=', self.class_id.id)])
            self.student_ids = [(6, 0, students.ids)]
    
    @api.constrains('due_date')
    def _check_due_date(self):
        for record in self:
            if record.due_date and record.due_date < fields.Date.today():
                raise ValidationError(_("The due date cannot be in the past."))

    