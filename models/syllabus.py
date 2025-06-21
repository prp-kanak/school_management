from odoo import models, fields, api

class Syllabus(models.Model):
    _name = 'syllabus.syllabus'
    _description = 'Class Syllabus'

    name = fields.Char(string='Title', required=True)
    class_id = fields.Many2one('school.standard', string='Class', required=True)
    subject_id = fields.Char( string='Subject', required=True)
    description = fields.Text(string='Syllabus Details')
    exam_ids = fields.One2many('exam.schedule', 'syllabus_id', string='Related Exams')

class Exam(models.Model):
    _inherit = 'exam.schedule'

    syllabus_id = fields.Many2one('syllabus.syllabus', string='Syllabus')
