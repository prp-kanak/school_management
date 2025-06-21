from odoo import models, fields, api, exceptions
from datetime import timedelta, date

class SchoolInquiry(models.Model):
    _name = 'school.inquiry'
    _description = 'School Inquiry'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Inquiry Title', required=True, tracking=True)
    student_name = fields.Char(string='Student', help="Link to a student if inquiry is about one.")
    contact_no = fields.Char(string='Contact', help="Parent or Guardian")
    inquiry_date = fields.Date(string='Inquiry Date', default=fields.Date.today(), required=True, readonly=True)
    state = fields.Selection(
        [('new', 'New'), ('in_progress', 'In Progress'), ('closed', 'Closed')],
        string='Status',
        default='new',
        tracking=True
    )
    description = fields.Text(string='Description')
    response = fields.Text(string='Response')
    priority = fields.Selection(
        [('low', 'Low'), ('medium','Medium'), ('high', 'High')],
        string='Priority',
        default='medium',
        tracking=True
    )
    expected_follow_up_date = fields.Date(
        string='Follow-up Date',
        compute='_compute_follow_up_date',
        store=True
    )
    overdue = fields.Boolean(
        string='Overdue',
        compute='_compute_overdue',
        store=True
    )
    follow_up_count = fields.Integer(
        string='Follow-up Count',
        compute='_compute_follow_up_count'
    )
    team_head_id = fields.Many2one('res.users',string="Team Leader",tracking=True)


    @api.depends('inquiry_date')
    def _compute_follow_up_date(self):
        for record in self:
            record.expected_follow_up_date = record.inquiry_date + timedelta(days=7) if record.inquiry_date else False

    @api.depends('expected_follow_up_date')
    def _compute_overdue(self):
        today = date.today()
        for record in self:
            record.overdue = record.expected_follow_up_date and record.expected_follow_up_date < today and record.state != 'closed'

    @api.depends('activity_ids')
    def _compute_follow_up_count(self):
        for record in self:
            record.follow_up_count = len(record.activity_ids)

    @api.constrains('inquiry_date', 'expected_follow_up_date')
    def _check_dates(self):
        for record in self:
            if record.expected_follow_up_date and record.inquiry_date > record.expected_follow_up_date:
                raise exceptions.ValidationError("Follow-up date cannot be before the inquiry date.")

    def action_close(self):
        for record in self:
            record.state = 'closed'
            record.message_post(body="Inquiry has been closed.")

