import math
from odoo import http
from odoo.http import request
from psycopg2 import IntegrityError

class CustomMenuController(http.Controller):
    @http.route('/schoolmanagement', auth='public', website=True)
    def custom_page(self, **kwargs):
        return request.render('school_management.template_custom_page', {})


class SchoolManagement(http.Controller):
    @http.route('/students', type='http', auth='public', website=True)
    def student_profile(self, **kwargs):
        all_students = request.env['student.student'].search([])
        return request.render('school_management.view_students_template', {
            'students': all_students,
        })


    # @http.route('/teachers', type='http', auth='public', website=True)
    # def teacher_profile(self, **kwargs):
    #     teacher = request.env['teacher.teacher'].sudo().search([])
    #     return request.render('school_management.view_teacher_template', {
    #         'teachers': teacher,
    #     })

    @http.route('/teachers', type='http', auth='public', website=True)
    def teacher_profile(self, page=1, **kwargs):
        try:
            page = int(page)  
        except ValueError:
            page = 1 

        per_page = 9 
        offset = (page - 1) * per_page
        teachers = request.env['teacher.teacher'].sudo().search([], offset=offset, limit=per_page)
        total_teachers = request.env['teacher.teacher'].sudo().search_count([])
        
        return request.render('school_management.view_teacher_template', {
            'teachers': teachers,
            'current_page': page,
            'total_pages': math.ceil(total_teachers / per_page),
        })

    @http.route('/teachers/add_teacher', type='http', auth='public', website=True)
    def add_teacher(self, **kwargs):
        return request.render('school_management.add_teacher_template', {})


    # @http.route('/teachers/add_teacher/submit-teacher', type='http', auth='public', website=True, methods=['POST'])
    # def submit_teacher(self, **kwargs):
    #     if kwargs:
    #         salary = kwargs.get('salary')
    #         if not salary or float(salary) <= 0:
    #             return request.redirect('/teachers/add_teacher?error=Salary must be greater than 0')
                
    #         request.env['teacher.teacher'].sudo().create({
    #             'name': kwargs.get('name'),
    #             'email': kwargs.get('email'),
    #             'phone': kwargs.get('phone'),
    #             'salary': float(kwargs.get('salary', 0.0)),  
    #         })
    #     return request.redirect('/teachers') 

    @http.route('/teachers/add_teacher/submit-teacher', type='http', auth='public', website=True, methods=['POST'])
    def submit_teacher(self):
        params = request.params  
        
        salary = params.get('salary')
        if not salary or float(salary) <= 0:
            return request.redirect('/teachers/add_teacher?error=Salary must be greater than 0')
        
        resume = request.httprequest.files.get('resume')
        resume_data = resume.read() if resume else None
        resume_base64 = base64.b64encode(resume_data).decode() if resume_data else None
        mimetype = resume.mimetype if resume and hasattr(resume, 'mimetype') else 'application/octet-stream'

        request.env['teacher.teacher'].sudo().create({
            'name': params.get('name'),
            'email': params.get('email'),
            'phone': params.get('phone'),
            'salary': float(params.get('salary', 0.0)),
        })

        if resume_base64:
            request.env['ir.attachment'].sudo().create({
                'name': resume.filename,
                'datas': resume_base64, 
                'res_model': 'teacher.teacher', 
                'res_id': teacher.id,  
                'mimetype': resume.mimetype, 
            })

        return request.redirect('/teachers') 

    @http.route('/teachers/edit_teacher/<int:teacher_id>', type='http', auth='public', website=True)
    def edit_teacher(self, teacher_id, **kwargs):
        teacher = request.env['teacher.teacher'].sudo().browse(teacher_id)
        if not teacher.exists():
            return request.not_found()
        return request.render('school_management.edit_teacher_template', {
            'teacher': teacher,
        })

    @http.route('/teachers/update_teacher/<int:teacher_id>', type='http', auth='public', website=True, methods=['POST'])
    def update_teacher(self, teacher_id, **kwargs):
        teacher = request.env['teacher.teacher'].sudo().browse(teacher_id)
        if not teacher.exists():
            return request.not_found()
        teacher.write({
            'name': kwargs.get('name'),
            'email': kwargs.get('email'),
            'phone': kwargs.get('phone'),
            'salary': float(kwargs.get('salary', 0.0)),
        })
        return request.redirect('/teachers')

 

    @http.route('/classes/class_records', type='http', auth='public', website=True)
    def class_records_page(self, **kwargs):
        class_records = request.env['school.class.record'].sudo().search([])
        return request.render('school_management.view_class_record_template', {
            'class_record': class_records,
        })


    @http.route('/classes/class_records/<int:record_id>', type='http', auth='public', website=True)
    def view_class_details(self,record_id, **kwargs):
        class_record = request.env['school.class.record'].sudo().browse(record_id)
        if not class_record.exists():
            return request.not_found()
        
        return request.render('school_management.view_class_detail_template', {
            'class_records': class_record,
        })


    @http.route('/standards', type='http', auth='public', website=True)
    def view_all_standards(self):
        standards = request.env['school.standard'].sudo().search([])
        return request.render('school_management.standards_template', {
            'standards': standards,
        })

    @http.route('/school/<string:class_name>', type='http', auth='public', website=True)
    def view_class_students(self, class_name):
        school_class = request.env['school.standard'].sudo().search([('name', '=', class_name)], limit=1)
        if not school_class:
            return request.not_found()
        
        students = request.env['student.student'].sudo().search([('class_id', '=', school_class.id)])
        return request.render('school_management.class_students_template', {
            'class_name': class_name,
            'students': students,
        })


class PortalCustom(http.Controller):
    @http.route('/my/inquiries', type='http', auth='public', website=True)
    def portal_inquiries(self, **kwargs):
        inquiries = request.env['school.inquiry'].sudo().search([])
        return request.render('school_management.portal_inquiries_template', {
            'inquiries': inquiries
        })


class ExamJSONController(http.Controller):

    @http.route('/api/exams', type='json', auth='public', methods=['POST'])
    def get_all_exams(self):
            exams = request.env['exam.schedule'].sudo().search([])

            if not exams:
                return {'status': 'error', 'message': 'No exams found.'}

            exam_data = []
            for exam in exams:
                exam_data.append({
                    'id': exam.id,
                    'name': exam.name,
                    'date': exam.date.strftime('%Y-%m-%d') if exam.date else None,
                    'class_name': exam.class_id.name if exam.class_id else None,
                    'subject': exam.subject,   
                    'supervisor_name': exam.supervisor_id.name if exam.supervisor_id else None,
                })

            return {'status': 'success', 'data': exam_data}

class StudentRpcTest(http.Controller):

    @http.route('/student/data', type='json', auth='public')
    def get_students(self):
        students = request.env['student.student'].search_read([], ['name', 'roll_number'])
        return students


    # @http.route('/student/create', type='json', auth='public')
    # def create_student(self, **kwargs):
    #         student_data = {
    #             'name': kwargs.get('name'),
    #             'age': kwargs.get('age'),
    #             'roll_number': kwargs.get('roll_number'),
    #         }
    #         new_student = request.env['student.student'].sudo().create(student_data)
    #         return {'success': True, 'student_id': new_student.id}
    #     