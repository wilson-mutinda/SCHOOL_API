from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    # get a token and login
    path('user_login/', views.user_login_view, name='user_login'),
    # refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Admin Roles
    path('create_custom_user/', views.list_create_custom_user_view, name='custom_user'),
    # create an admin
    path('create_admin/', views.create_admin_view, name='admin'),
    # view admin
    path('admin_info/<int:pk>/', views.retreive_update_delete_admin_view, name='admin_info'),
    # custom user by role_id
    path('custom_user_info/<int:role_id>/', views.retreive_update_delete_custom_user_view, name='custom_user_info'),
    # get the number of custom users
    path('number_of_custom_users/', views.retreive_number_of_custom_users_view, name='number_of_custom_users'),
    # retreive the number of teachers
    path('all_teachers/', views.get_the_number_of_registered_teachers, name='all_teachers'),
    # retreive all teachers
    path('fetch_all_teachers/', views.fetch_all_teachers_view, name='fetch_all_teachers'),
    # retreive all students
    path('fetch_all_students/', views.fetch_all_students_view, name='fetch_all_students'),
    # retreive all parents
    path('fetch_all_parents/', views.fetch_all_parents_view, name='fetch_all_parents'),
    # retreive the number of parents
    path('all_parents/', views.retreive_number_of_parents_view, name='all_parents'),
    # retreive the number of students
    path('all_students/', views.retreive_number_of_students_view, name='all_students'),
    # create role
    path('create_role/', views.list_create_role_view, name='roles'),
    # retreive and update the role
    path('role_info/<int:pk>/', views.retreive_update_delete_role_view, name='role_info'),
    # create announcement
    path('create_announcement/', views.create_announcement_admin_view, name='announcement'),
    # retreive the number of announcements
    path('all_announcements/', views.retreive_number_of_announcements_view, name='all_announcements'),
    # retreive admin targeted announcements
    path('admin_targeted_announcements/', views.retreive_admin_targeted_announcements_view, name='admin_targeted_announcements'),
    # retreive teacher targeted announcements
    path('teacher_targeted_announcements/', views.retreive_teacher_targeted_announcements_view, name='teacher_targeted_announcements'),
    # retreive student targeted announcements
    path('student_targeted_announcements/', views.retreive_student_targeted_announcements_view, name='student_targeted_announcements'),
    # retreive parent targeted announcements
    path('parent_targeted_announcements/', views.retreive_parent_targeted_announcements_view, name='parent_targeted_announcements'),
    # create term
    path('create_term/', views.create_term_view, name='terms'),
    # retreive and update term
    path('term_info/<str:name>/', views.retreive_update_delete_term_view, name='term_info'),
    # retreive update cat
    path('cat_details_admin/<str:cat_code>/', views.retreive_update_delete_cat_admin_view, name='cat_details_admin'),
    # retreive reportform
    path('report_form_admin_info/<str:student_code>/', views.retreive_update_delete_reportform_admin_view, name='report_form_admin'),
    # create an exam
    path('create_exam_admin/', views.create_retreive_exam_view, name='exam_admin'),
    # retreive all exams
    path('all_exams/', views.retreive_update_delete_exam_view, name='all_exams'),

    # Teacher Roles
    # Techer to creaate announcement
    path('create_announcement_teacher/', views.create_announcement_teacher_view, name='announcement_teacher'),
    # Get the student exam results
    path('student_results/<str:student>/', views.get_student_exam_marks_admin_teacher_view, name='student_results'),
    # create exam
    path('create_exam_teacher/', views.create_retreive_exam_view, name='exam_teacher'),

    path('create_teacher/', views.create_teacher_view, name='teacher'),
    path('create_parent/', views.create_parent_view, name='parent'),
    path('create_student/', views.create_student_view, name='student'),
    path('create_subject/', views.create_subject_view, name='subject'),
    path('create_class/', views.create_class_view, name='class'),
    path('create_stream/', views.create_class_stream_view, name='stream'),
    path('create_cat/', views.create_cat_view, name='cat'),
    path('create_cat_grade/', views.create_cat_grade_view, name='cat_grade'),
    path('create_exam/', views.create_retreive_exam_view, name='exam'),
    path('create_exam_grade/', views.create_exam_grade_view, name='exam_grade'),
    path('create_exam_and_cat/', views.create_exam_and_cat_view, name='exam_and_cat'),
    path('create_class_stream_subject/', views.create_class_stream_subject_view, name='class_stream_subject'),
    path('create_overall_subject_grade/', views.create_overall_subject_grade_view, name='overall_suject_grade'),
    path('create_final_grade/', views.create_final_grade_view, name='final_grade'),
    path('create_report_form/', views.create_report_form_view, name='report_form'),
    path('teacher_info/<int:pk>/', views.retreive_update_destoy_teacher_info_view, name='teacher_info'),
    path('student_info/<int:pk>/', views.retreive_update_delete_student_info_view, name='student_info'),
    path('parent_info/<int:pk>/', views.retreive_update_delete_parent_info_view, name='parent_info'),
    path('report_form_teacher_admin/<str:student_code>/', views.retreive_update_delete_report_form_admin_teacher_view, name='report_form_admin_teacher'),
    path('report_form_parent/<str:student_code>/', views.retreive_update_delete_report_form_parent_view, name='report_form_parent'),
    path('class_info/<int:pk>/', views.retreive_update_delete_class_view, name='class_info'),
    path('stream_info/<int:pk>/', views.retreive_update_delete_stream_info_view, name='stream_info'),
]
