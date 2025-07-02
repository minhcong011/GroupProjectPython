
from django.urls import path
from . import views
from cv import views as cv_views

urlpatterns = [
    path('lectures/create/', views.create_lecture, name='create_lecture'),
    path('lectures/', views.lecture_list, name='lecture_list'),
    path('course_management/', views.course_management, name='course_management'),

    # Assignment management
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/create/', views.create_assignment, name='create_assignment'),
    path('assignments/<int:assignment_id>/add_questions/', views.add_questions, name='add_questions'),
    path('assignments/<int:assignment_id>/delete/', views.delete_assignment, name='delete_assignment'),

    path('cv/', cv_views.cv_edit, name='cv_edit'),
    path('cv/password/', cv_views.password_2fa, name='password_2fa'),
]
