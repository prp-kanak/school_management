from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import AccessError
from odoo.exceptions import UserError
from datetime import date
import qrcode
import base64
from io import BytesIO

class StudentStudent(models.Model):
    _name = "student.student"
    _description = "Students"
    _inherit = ['mail.thread', 'mail.activity.mixin','mixin.model']


    # employee = fields.Many2one('hr.employee')
    # contact = fields.Many2one('res.partner')

    # name = fields.Char(required=True)
    # student_name = fields.Many2one( string="Students names")
    address = fields.Text()
    age = fields.Integer()
    weight = fields.Float(default=50.0)
    birth_date = fields.Date()
    status = fields.Selection(
        [('passed', 'Passed'),('failed', 'Failed')],
        string="Status",
        default='passed',
        required=True,
    )
    gender = fields.Selection([
             ('male', 'Male'),
             ('female', 'Female')])
    notes = fields.Text(string="Notes")
    section = fields.Selection(
        [('a', 'A'), ('b', 'B'), ('c','C')],
        string="Section",
        default='a',
        required=True,
    )
    active = fields.Boolean(string='Active', default=True)

    team_head_id = fields.Many2one('res.users',string="Team Leader",help="Head of the team",tracking=True)

    attachment_ids = fields.Many2many(
        'ir.attachment', string="Attachments",
        help="Attach documents related to the student."
    )
    id_proof = fields.Binary(string="ID Proof")
    id_proof_filename = fields.Char(string="ID Proof Filename")

    birth_certificate = fields.Binary(string="Birth Certificate")
    birth_certificate_filename = fields.Char(string="Birth Certificate Filename")

    transfer_certificate = fields.Binary(string="Transfer Certificate")
    transfer_certificate_filename = fields.Char(string="Transfer Certificate Filename")

    mark_sheet = fields.Binary(string="Mark Sheet")
    mark_sheet_filename = fields.Char(string="Mark Sheet Filename")

    fee_receipt = fields.Binary(string="Fee Receipt")
    fee_receipt_filename = fields.Char(string="Fee Receipt Filename")
    
    is_fav = fields.Boolean(default=False, help="Mark as favorite student.")
    profile_picture = fields.Binary(string="Profile Picture")
    contact_number = fields.Char(string="Contact Number")
    email = fields.Char(string="Email Address")
    blood_group = fields.Selection([
        ('a+', 'A+'), 
        ('a-', 'A-'), 
        ('b+', 'B+'), 
        ('b-', 'B-'), 
        ('ab+', 'AB+'), 
        ('ab-', 'AB-'), 
        ('o+', 'O+'), 
        ('o-', 'O-')
    ], string="Blood Group")
    disability = fields.Selection([('yes','Yes'),('no','No')],string="Disability")
    roll_number = fields.Char(string="Roll Number")
    class_id = fields.Many2one('school.standard', string="Class", required=True) 
    admission_date = fields.Date(string="Date of Admission")
    previous_grade = fields.Char(string="Previous Grade/Class")
    board = fields.Selection(
    [('cbse', 'CBSE'), ('icse', 'ICSE'), ('state', 'State Board'), ('international', 'International')],
    string="Board/University"
    )
    religion = fields.Selection(
    [
        ('hindu', 'Hindu'),
        ('muslim', 'Muslim'),
        ('christian', 'Christian'),
        ('sikh', 'Sikh'),
        ('jain', 'Jain'),
        ('other', 'Other'),
    ],
    string="Religion",
    help="Select the student's religion."
    )
    caste_category = fields.Selection(
    [
        ('general', 'General'),
        ('obc', 'OBC'),
        ('ews', 'EWS'),
        ('sc', 'SC'),
        ('st', 'ST'),
        ('other', 'Other'),
    ],
    string="Caste Category",
    help="Select the student's caste or category."
    )
    admission_test_score = fields.Float(string="Admission Test Score")
    transportation_required = fields.Selection([('yes','Yes'),('no','No')],
    string="Transportation Required", default=False)

    father_name = fields.Char(string="Father's Name")
    father_contact = fields.Char(string="Father's Contact Number")
    father_occupation = fields.Char(string="Father's Occupation")
    mother_name = fields.Char(string="Mother's Name")
    mother_contact = fields.Char(string="Mother's Contact Number")
    mother_occupation = fields.Char(string="Mother's Occupation")
    # stage = fields.Selection(
    #     [
    #         ('enrolled', 'Enrolled'),
    #         ('on_hold', 'On Hold'),
    #         ('completed', 'Completed'),
    #     ],
    #     string="Stage",
    #     default='enrolled',
    # )
    total_fees = fields.Float(string="Total Fees", required=True)
    fees_paid = fields.Float(string="Fees Paid")
    fees_due = fields.Float(string="Fees Due", compute="_compute_fees_due", store=True, readonly=True)
    last_payment_date = fields.Date(string="Last Payment Date")
    qr_code_url = fields.Binary("QR Code", compute="_compute_qr_code_url", store=False)

    # def write(self, vals):
    #     if 'total_fees' in vals:
    #         raise ValidationError("You are not allowed to modify the total fees.")
    #     return super(StudentStudent, self).write(vals)


    teacher_id = fields.Many2one(
        'teacher.teacher',
        string="Class Teacher",
        help="The teacher responsible for this student."
    )
    total_marks = fields.Float(string="Total Marks", compute="_compute_total_marks", store=True)
    exam_ids = fields.One2many(
        'exam.exam', 'student_id', string='Exams'
    )
    scheduled_exam_count = fields.Integer(
        string="Scheduled Exam Count",
        compute="_compute_scheduled_exam_count",
    )
    avg_weight = fields.Float(compute="_compute_avg_weight", string="Average Weight")
    class_record_id = fields.Many2one(
        'school.class.record',
        string="Class Record",
        help="The class record this student is associated with."
    )
    create_date = fields.Datetime(string="Created On", readonly=True)
    



    #CREATE IN CREATE
    # def create(self, vals):
    #     res = super(StudentStudent, self).create(vals)
    #     new_employee = self.env['hr.employee'].create(
    #         {
    #             'name': res.name
    #         }
    #     )
    #     res.employee = new_employee.id
    #     new_contact = self.env['res.partner'].create(
    #         {
    #             'name': res.name
    #         }
    #     )
    #     res.contact = new_contact.id
    #     return res


    #WRITE
    # def write(self, vals):
    #     res = super(StudentStudent, self).write(vals)
    #     self.employee.write({'name': self.name})
    #     self.contact.write({'name': self.name})
    #     return res


    #UNLINK
    # def unlink(self):
    #     self.employee.unlink()
    #     self.contact.unlink()
    #     res = super(StudentStudent, self).unlink()
    #     return res


    #CREATE IN WRITE(write in existing code and it create a new updated record)
    # def write(self,vals): 
    #     res = super(StudentStudent, self).write(vals)
    #     self.employee.create({'name': self.name})
    #     self.contact.create({'name': self.name})
    #     return res 


    #WRITE IN CREATE(In comment field the data is automatically entered when new student is created)
    # def create(self, vals):
    #     res = super(StudentStudent, self).create(vals)
    #     new_employee = self.env['hr.employee'].create({'name': res.name})
    #     new_contact = self.env['res.partner'].create({'name': res.name})
    #     res.write({
    #         'employee': new_employee.id,
    #         'contact': new_contact.id,
    #         })
    #     new_contact.write({'comment': f"Record created for {res.name}"})
    #     return res



    # @api.model
    # def create(self,vals):
    #     print("***************** before super call vals",vals) #remains same
    #     print("+++++++++++++++++++++++ before super call self",self)#gives model name without id
    #     res = super(StudentStudent,self).create(vals)
    #     print("+++++++++++++++++++++++ after super call self",self)#gives model name without id 
    #     print("***************** after super call vals",vals)#remians same 
    #     print("+++++++++++++++++++++++ after super call res",res)# returns recordset ID
    #     return res
        

    # def write(self,vals):
    #     print("+++++++++++++++++++++++ before super call self",self.name)#gives old name
    #     print("***************** before super call vals",vals)#returns dict with updated value
    #     res = super(StudentStudent,self).write(vals)
    #     print("+++++++++++++++++++++++ after super call self",self.name)#gives updated name
    #     # print("+++++++++++++++++++++++ after super call self",self)#gives recordset id 
    #     print("***************** after super call vals",vals)#same dict with updated value
    #     print("---------------- res",res)#true or false
    #     return res


    # def unlink(self):
    #     print("________________________before super call self", self.name)#record deleted
    #     # print("________________________before super call vals", vals)
    #     res = super(StudentStudent,self).unlink()
    #     # print("-------------------------after super call self", self.name)#error as record already deleted
    #     print("++++++++++++++++++++++++++after super call self", self)#returns recordset id 
    #     # print("-------------------------after super call vals", vals)
    #     print("-------------------------res", res)#true or false
    #     return res

    @api.depends('exam_ids.marks_obtained') 
    def _compute_total_marks(self):
        for student in self:
            student.total_marks = sum(exam.marks_obtained for exam in student.exam_ids)

    @api.depends('total_fees', 'fees_paid')
    def _compute_fees_due(self):
        for record in self:
            record.fees_due = record.total_fees - record.fees_paid


    # @api.depends('weight', 'age')
    # def _compute_avg_weight(self):
    #     for rec in self:
    #         rec.avg_weight = sum(student.weight for student in self.search([('age', '=', rec.age)])) / len(self.search([('age', '=', rec.age)]))

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError("Invalid email address: %s" % record.email)

    @api.constrains('admission_date')
    def _check_admission_date(self):
        for record in self:
            if record.admission_date and record.admission_date > date.today():
                raise ValidationError("The Date of Admission cannot be a future date. Please enter a valid date.")

    @api.constrains('birth_date', 'admission_date')
    def _check_birth_date_gap(self):
        for record in self:
            if record.birth_date and record.admission_date:
                age_at_admission = record.admission_date.year - record.birth_date.year
                if (record.admission_date.month, record.admission_date.day) < (record.birth_date.month, record.birth_date.day):
                    age_at_admission -= 1
                if age_at_admission < 3:
                    raise ValidationError(
                        "The gap between the birth date and the admission date must be at least 3 years."
                    )

    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 5:
            self.notes = "Student is too young for admission."

    # @api.onchange('status')
    # def _onchange_status(self):
    #     if self.status == 'failed':
    #         self.notes = "Student has failed. Consider suggesting additional support or guidance."
    #     elif self.status == 'passed':
    #         self.notes = "Student has passed. Encourage them to continue performing well."


    _sql_constraints = [
    ('unique_roll_number_class',
     'UNIQUE(roll_number, class_id)',
     'The roll number must be unique within the same class.'),
    ]

    

    def action_suspend(self):
        self.write({'active': False})
    

    def _compute_scheduled_exam_count(self):
        for student in self:
            student.scheduled_exam_count = self.env['exam.schedule'].search_count(
                [('student_ids', '=', student.id)]
            )

    def action_open_scheduled_exams(self):
        self.ensure_one()
        return {
            'name': 'Scheduled Exams',
            'type': 'ir.actions.act_window',
            'res_model': 'exam.schedule',
            'view_mode': 'list,form',
            'domain': [('student_ids', '=', self.id)],
            'context': dict(self._context, default_student_ids=self.id),
        }


    def get_binary_field_value(self, field, record_id):
        restricted_fields = [
            'id_proof', 'birth_certificate', 'transfer_certificate',
            'mark_sheet', 'fee_receipt'
        ]
        if field in restricted_fields:
            raise AccessError(_("You do not have permission to download this document."))
        return super(Student, self).get_binary_field_value(field, record_id)


    
    def _compute_qr_code_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for student in self:
            # URL to the doctor ID card report
            report_url = f"{base_url}/report/pdf/school_management.student_report_details/{student.id}"
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L)
            qr.add_data(report_url)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            student.qr_code_url = base64.b64encode(buffer.getvalue())


    @api.onchange('class_id')
    def _onchange_class_id(self):
        for record in self:
            if record.class_id:
                fees = self.env['fees.fees'].search([('class_id', '=', record.class_id.id)], limit=1)
                if fees:
                    record.total_fees = fees.amount
                else:
                    record.total_fees = 0.0

    @api.depends('total_fees', 'fees_paid')
    def _compute_fees_due(self):
        for record in self:
            record.fees_due = record.total_fees - record.fees_paid if record.total_fees else 0.0


    @api.model_create_multi
    def create(self, vals):
        if 'class_id' in vals:
            fees = self.env['fees.fees'].search([('class_id', '=', vals['class_id'])], limit=1)
            if fees:
                vals['total_fees'] = fees.amount
        return super(StudentStudent, self).create(vals)

    def write(self, vals):
        if 'class_id' in vals:
            fees = self.env['fees.fees'].search([('class_id', '=', vals['class_id'])], limit=1)
            if fees:
                vals['total_fees'] = fees.amount
        return super(StudentStudent, self).write(vals)


    def action_promote_student(self):
        for student in self:
            if student.status == 'failed':  
                raise ValidationError(
                    f"Student {student.name} cannot be promoted as their status is 'Failed'."
                )
            
            current_class = student.class_id
            next_class = self.env['school.standard'].search(
                [('sequence', '>', current_class.sequence)], 
                order='sequence asc', 
                limit=1
            )
            
            if not next_class:
                raise ValidationError(
                    f"No next class available for {current_class.name}. Promotion is not possible."
                )
            
            student.class_id = next_class.id



    def action_suspend(self):
            if not self.email:
                raise UserError(_("Student email is not set. Cannot send email."))

            message = _("The student has been suspended, and an email has been sent.")
            self.message_post(body=message)

            template_id = self.env.ref('school_management.email_template_student_suspend').id
            self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)