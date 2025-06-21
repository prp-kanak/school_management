from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ExamRecordsWizard(models.TransientModel):
    _name = 'exam.records.wizard'
    _description = 'Exam Records Wizard'

    class_id = fields.Many2one(
        'school.standard', 
        string='Class', 
        required=True,
        help='Select the class to view exam records.'
    )
    schedule_id = fields.Many2one(
        'exam.schedule', 
        string='Exam Name', 
        required=True,
        domain="[('class_id', '=', class_id)]",
        help='Select the exam name.'
    )
    student_result_ids = fields.One2many(
        'exam.records.wizard.line', 
        'wizard_id', 
        string='Student Results',
        readonly=True
    )

    @api.onchange('schedule_id')
    def _onchange_schedule_id(self):
        if self.schedule_id:
            results = self.env['exam.result'].search([('schedule_id', '=', self.schedule_id.id)])
            _logger.info("Exam Results Found: %s", results)
            lines = []
            for result in results:
                _logger.info("Processing Result: %s", result)
                for student_line in result.student_addline:
                    _logger.info("Adding Student Line: Name=%s, Marks=%s", student_line.student_name.name, student_line.marks_gained)
                    lines.append((0, 0, {
                        'student_name': student_line.student_name.name,
                        'marks_gained': student_line.marks_gained,
                    }))
            self.student_result_ids = lines
            _logger.info("Final Student Result Lines: %s", self.student_result_ids)
        else:
            self.student_result_ids = [(5, 0)]

    def print_report(self):
        self.ensure_one()
        _logger.info("Wizard Data: %s", self.read())
        for line in self.student_result_ids:
            _logger.info("Line Data: %s", line.read())
        return self.env.ref('school_management.action_report_exam_records').report_action(self)

class ExamRecordsWizardLine(models.TransientModel):
    _name = 'exam.records.wizard.line'
    _description = 'Exam Records Wizard Line'

    wizard_id = fields.Many2one('exam.records.wizard', string='Wizard Reference', required=True)
    student_name = fields.Char(string='Student Name', readonly=True)
    marks_gained = fields.Float(string='Marks Gained', readonly=True)
