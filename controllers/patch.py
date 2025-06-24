from odoo import http
from odoo.http import request

class StudentController(http.Controller):
    @http.route('/student/update/<int:student_id>', type='json', auth='user', methods=['PATCH'])
    def update_student(self, student_id, **kwargs):
        
        Student = request.env['student.student'].sudo()
        student = Student.browse(student_id)

        if not student.exists():
            return {"error": f"Student with ID {student_id} not found."}

        student.write(kwargs)
        return {"success": True, "message": "Student updated successfully.", "student_id": student_id}
