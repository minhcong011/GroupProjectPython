
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


    path('cv/', cv_views.cv_edit, name='cv_edit'),
    path('cv/password/', cv_views.password_2fa, name='password_2fa'),

    path('course_management/', views.course_management, name='course_management'),
    path('create_course/', views.create_course, name='create_course'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
     path('khoa-hoc/', views.khoa_hoc, name='khoa_hoc'),

]