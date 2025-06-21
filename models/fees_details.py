from odoo import fields, models, api
from datetime import date

class FeesFees(models.Model):
    _name = "fees.fees"
    _description = "Student Fees Details"

    class_id = fields.Many2one('school.standard', string="Class", required=True)
    term_1 = fields.Monetary(string="Term 1", required=True)
    term_2 = fields.Monetary(string="Term 2", required=True)
    exam_fees = fields.Monetary(string="Exam fees", required=True)
    amount = fields.Monetary(string="Total Amount", required=True, compute="_compute_total_amount")
    currency_id = fields.Many2one('res.currency', string="Currency", required=True, default=lambda self: self.env.company.currency_id)
    due_date = fields.Date(string="Due Date", required=True)
    late_fees = fields.Monetary(string="Fixed Late Fees", help="Fixed penalty fee for late payment.")
    total_amount_with_fine = fields.Monetary(string="Total with Fine", compute="_compute_total_with_fine", store=True)
    description = fields.Text(string="Description", help="Additional information about the fees.")
    active = fields.Boolean(string="Active", default=True)

    @api.depends('term_1', 'term_2', 'exam_fees', 'late_fees')
    def _compute_total_with_fine(self):
        for record in self:
            term_1 = record.term_1 or 0
            term_2 = record.term_2 or 0
            exam_fees = record.exam_fees or 0
            late_fees = record.late_fees or 0
            
            record.total_amount_with_fine = term_1 + term_2 + exam_fees + late_fees

    @api.depends('term_1','term_2','exam_fees')
    def _compute_total_amount(self):
        for record in self:
            term_1 =record.term_1 or 0
            term_2 =record.term_2 or 0
            exam_fees = record.exam_fees or 0

            record.amount = term_1 + term_2 + exam_fees


            