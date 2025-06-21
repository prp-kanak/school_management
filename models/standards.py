from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import AccessError


class SchoolStandard(models.Model):
    _name = 'school.standard'
    _description = 'Class/Standard'
    _inherit = ['mail.thread']
    _order = 'sequence asc'  # Order classes by sequence in ascending order


    name = fields.Char(string="Class Name")
    section = fields.Selection(
        [('a', 'A'), ('b', 'B'), ('c','C')],
        string="Section",
    )
    class_teacher_id = fields.Many2one('teacher.teacher', string="Class Teacher")
    student_ids = fields.One2many('student.student', 'class_id', string="Students",readonly=True)
    timetable_ids = fields.One2many('school.timetable', 'class_id', string="Timetables")
    record_ids = fields.One2many('school.class.record', 'class_id', string="Class Records")
    _is_closed = fields.Boolean(string="Is Closed", default=False)
    student_count = fields.Integer(
        string="Number of Students",
        compute="_compute_student_count",
        store=True
    )
    sequence = fields.Integer(string="Sequence", help="Order of the class.")

    #server action
    @api.model
    def assign_sequence(self):
        all_classes = self.search([], order='name asc')  # Fetch all records sorted by 'name'
        sequence = 1  # Start the sequence from 1
        for standard in all_classes:
            standard.sequence = sequence  # Assign the sequence number
            sequence += 1  # Increment the sequence for the next record


    @api.depends('student_ids')
    def _compute_student_count(self):
        for standard in self:
            standard.student_count = len(standard.student_ids)

 
    # @api.model_create_multi
    # def create(self, vals):
    #     if not vals.get('name'):
    #         vals['name'] = 'No class name provided.'
    #     if not vals.get('section'):
    #         vals['section'] = 'a'  # Default section if not provided

    #     record = super().create(vals)
    #     return record
   


    def write(self, vals):
        protected_fields = {'name', 'section', 'class_teacher_id', 'student_ids'}
        
        for record in self:
            if record._is_closed and any(field in vals for field in protected_fields):
                raise UserError("You cannot modify key details of a closed class. Please reopen it if changes are required.")
        
        return super().write(vals)


    # def read(self, fields=None, load='_classic_read'):
    #     result = super(SchoolStandard, self).read(fields=fields, load=load)
    #     for record in result:
    #         class_teacher_id = record.get('class_teacher_id')
    #         teacher_name = ''
    #         if class_teacher_id:
    #             teacher_name = self.env['teacher.teacher'].browse(class_teacher_id).name
            
    #         class_name = record.get('name', 'No Name')
    #         section = record.get('section', 'No Section')
            
    #         record['class_summary'] = f"Class '{class_name}' in Section '{section}' taught by {teacher_name}"
    #         print(record['class_summary'])
    #     return result


    def unlink(self):
        for record in self:
            if record.student_ids:
                raise UserError(f"Cannot delete the class '{record.name}' because it has students assigned. Please remove the students before deleting.")
        
        return super().unlink()




    
