
from django.urls import path
from . import views
from cv import views as cv_views

urlpatterns = [
    path('lectures/create/', views.create_lecture, name='create_lecture'),
    path('lectures/', views.lecture_list, name='lecture_list'),
    path('lectures/<int:pk>/', views.lecture_detail, name='lecture_detail'),
    path('lectures/<int:pk>/edit/', views.edit_lecture, name='edit_lecture'),
    path('lectures/<int:pk>/delete/', views.delete_lecture, name='delete_lecture'),

    path('course_management/', views.course_management, name='course_management'),

    # Assignment management
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/create/', views.create_assignment, name='create_assignment'),
    path('assignments/<int:assignment_id>/add_questions/', views.add_questions, name='add_questions'),
    path('questions/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('questions/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('assignments/<int:assignment_id>/edit/', views.edit_assignment, name='edit_assignment'),
    path('assignments/<int:assignment_id>/delete/', views.delete_assignment, name='delete_assignment'),

    # Grading system
    path('cham-diem/', views.cham_diem, name='cham_diem'),
    path('chi-tiet-bai-tap/<int:bai_tap_id>/', views.chi_tiet_bai_tap, name='chi_tiet_bai_tap'),
    path('cham-bai-trac-nghiem/<int:bai_lam_id>/', views.cham_bai_trac_nghiem, name='cham_bai_trac_nghiem'),
    path('cham-bai-lap-trinh/<int:bai_lam_id>/', views.cham_bai_lap_trinh, name='cham_bai_lap_trinh'),
    path('quan-ly-test-case/<int:bai_tap_id>/', views.quan_ly_test_case, name='quan_ly_test_case'),
    path('tao-test-case-tu-dong/<int:bai_tap_id>/', views.tao_test_case_tu_dong, name='tao_test_case_tu_dong'),
    path('xoa-test-case/<int:test_case_id>/', views.xoa_test_case, name='xoa_test_case'),
    path('ket-qua-cham-diem/<int:bai_lam_id>/', views.ket_qua_cham_diem, name='ket_qua_cham_diem'),
    path('sua-diem/<int:bai_lam_id>/', views.sua_diem, name='sua_diem'),
    path('download-file/<int:bai_lam_id>/', views.download_file, name='download_file'),

    # Debug
    path('debug-csrf/', views.debug_csrf, name='debug_csrf'),
    path('test-create-assignment/', views.test_create_assignment, name='test_create_assignment'),

    path('cv/', cv_views.cv_edit, name='cv_edit'),
    path('cv/password/', cv_views.password_2fa, name='password_2fa'),

    path('course_management/', views.course_management, name='course_management'),
    path('create_course/', views.create_course, name='create_course'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
 

]