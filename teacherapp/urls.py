from django.urls import path
from . import views
from cv import views as cv_views

urlpatterns = [
    path('lectures/create/', views.create_lecture, name='create_lecture'),
    path('lectures/', views.lecture_list, name='lecture_list'),
   
    path('cv/', cv_views.cv_edit, name='cv_edit'),
    path('cv/password/', cv_views.password_2fa, name='password_2fa'),

    path('course_management/', views.course_management, name='course_management'),
    path('create_course/', views.create_course, name='create_course'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
     path('khoa-hoc/', views.khoa_hoc, name='khoa_hoc'),

]