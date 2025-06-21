from odoo import models, fields, api
from odoo.exceptions import UserError

class PTMSchedule(models.Model):
    _name = 'ptm.schedule'
    _description = 'PTM Schedule'
    _inherit = ['mail.thread', 'mail.activity.mixin'] 


    name = fields.Char(string="PTM Title", required=True)
    class_id = fields.Many2one('school.standard', string="Standard", required=True)
    date = fields.Date(string="Meeting Date", required=True)
    start_time = fields.Float(string="Start Time", required=True)
    end_time = fields.Float(string="End Time", required=True)
    agenda = fields.Text(string="Agenda")
    student_ids = fields.One2many('ptm.student.schedule', 'ptm_id', string="Students Scheduled")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='draft')

    def action_set_scheduled(self):
        for record in self:
            if record.state == 'draft':
                record.state = 'scheduled'
            else:
                raise UserError("Can only schedule when in Draft state.")

    def action_set_completed(self):
        for record in self:
            if record.state == 'scheduled':
                record.state = 'completed'
            else:
                raise UserError("Can only complete when in Scheduled state.")

    def action_set_cancelled(self):
        for record in self:
            if record.state in ['draft', 'scheduled']:
                record.state = 'cancelled'
            else:
                raise UserError("Can only cancel when in Draft or Scheduled state.")


    @api.onchange('class_id')
    def _onchange_class_id(self):
        if self.class_id:
            students = self.env['student.student'].search([('class_id', '=', self.class_id.id)])
            self.student_ids = [(5, 0, 0)]  
            self.student_ids = [(0, 0, {'student_id': student.id}) for student in students]


class PTMStudentSchedule(models.Model):
    _name = 'ptm.student.schedule'
    _description = 'PTM Student Schedule'

    ptm_id = fields.Many2one('ptm.schedule', string="PTM Reference", required=True, ondelete='cascade')
    student_id = fields.Many2one('student.student', string="Student", required=True)
    parent_name = fields.Char(string="Parent Name")
    notification_sent = fields.Boolean(string="Notification Sent", default=False)
