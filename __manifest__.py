{
	'name':	'School',
	'version': '18.0.1.0',
	'category': 'School/School',
	'summary': 'School management',
    'description': """School app.""",
    'depends': ['base', 'mail','sale_management','website','portal','product','stock', 'sale', 'web', 'website_sale'],
    'data': 
        [ 
          # 'data/student_data.xml',
          # 'data/teacher_data.xml',
          'data/server_action_so.xml',
          'data/ir_cron_data.xml',
          'data/email_template_suspend.xml',
          'data/server_action_student.xml',
          'security/groups.xml',
          'security/ir.model.access.csv',
          # 'security/record_rules.xml',
        

          'report/sale_paragon_demo.xml',
          'report/student_record_template.xml',
          'report/student_id_template.xml',
          'report/sales_report_inherit.xml',
          'report/wizard_demo_template.xml',
          # 'report/hr_report_inherit.xml',
          'report/product_label_template_inherit.xml',
          'report/custom_product_product_template.xml',
          

          'views/menuitem_views.xml',
          'views/student_views.xml',
          # 'views/teacher_views.xml',
          'views/teacher_records_views.xml',
          'views/exam_schedule_views.xml',  
          'views/exam_results_views.xml',
          # 'views/exam_list_views.xml',
          'views/student_attendance.xml',
          'views/fees_details_views.xml',
          'views/school_standard_views.xml',
          'views/school_timetable_views.xml',
          'views/school_class_records_views.xml',
          'views/res_partner_views.xml',
          'views/sale_order_views.xml',
          'views/class_ptm_views.xml',
          'views/assingment_views.xml',
          'views/syllabus_views.xml',
          'views/inquiry_views.xml',
          'views/so_menu_confirm.xml',
         
        
          'views/website_menu.xml',
          'views/website_template.xml',
          'views/website_mega_menus.xml',
          'views/website_student_data.xml',
          'views/website_teacher_data.xml',
          'views/website_class_records.xml',
          'views/website_standards_data.xml',
          'views/website_class_student.xml',
          'views/portal_my_account.xml',
          # 'views/website_footer_template.xml',
          'views/website_home_form.xml',
          # 'views/website_so_page.xml',
          'views/website_stock_update.xml',
          'views/website_product_moq.xml',
          'views/website_product_carousel.xml',
                                  

          'views/snippets/options.xml',
          'views/snippets/s_snippet_name.xml',


          'wizard/so_report_views.xml',
          'report/exam_records_wizard_template.xml',
          'wizard/exam_records_wizard_views.xml',
          'wizard/product_label_extra_content.xml',


          'static/src/xml/lifecycle_template.xml',


        ],
    'installable': True,
    'application': True,
    'images': ['static/description/icon.png'],
    'assets': {

        'web.assets_frontend': [
            '/school_management/static/src/scss/snippet.scss',

            'school_management/static/src/js/lifecycle.js',
            'school_management/static/src/js/d_none_student.js',

            'school_management/static/src/js/student_orm_rpc.js',

            'school_management/static/src/js/student_create.js',

            'school_management/static/src/js/student_patch.js',

            'school_management/static/src/js/website_product_moq.js',
        ],

        'web.assets_backend': [
            'school_management/static/src/js/custom_widget.js',
            'school_management/static/src/xml/custom_widget_template.xml',

            'school_management/static/src/js/email_widget.js',
            'school_management/static/src/xml/email_widget_template.xml',


        ],
    },

    'license': 'OPL-1',
    'website': "https://www.kanakinfosystems.com",
    'author': "kanak",
}