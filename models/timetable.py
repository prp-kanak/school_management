from odoo import models, fields, api
from datetime import timedelta

class SchoolTimetable(models.Model):
    _name = 'school.timetable'
    _description = 'Weekly Timetable for Teachers'

    name = fields.Char(string="Title", required=True)  # e.g., "Math Class"
    teacher_id = fields.Many2one('teacher.teacher', string="Teacher", required=True)
    class_id = fields.Many2one('school.standard', string="Class", required=True)
    subject_id = fields.Char(string="Subject", required=True)
    start_datetime = fields.Datetime(string="Start Time", required=True)
    end_datetime = fields.Datetime(string="End Time", required=True)
    description = fields.Text(string="Description")

    @api.constrains('start_datetime', 'end_datetime')
    def _check_datetime(self):
        for record in self:
            if record.start_datetime >= record.end_datetime:
                raise models.ValidationError("End time must be after the start time.")


    @api.model_create_multi
    def create(self, vals):
        if not vals.get('teacher_id'):
            raise UserError('Teacher is required.')
        return super(SchoolTimetable, self).create(vals)


    @api.onchange('teacher_id')
    def _onchange_teacher(self):
        if self.teacher_id:
            self.subject_id = False  # Ensure valid resetting


    @api.depends('teacher_id')
    def _compute_some_field(self):
        for record in self:
            if not record.teacher_id:
                _logger.error('Teacher is missing for record ID %s', record.id)


