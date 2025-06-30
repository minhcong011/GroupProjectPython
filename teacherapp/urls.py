from django.urls import path
from . import views as teacher_views
from cv import views as cv_views

urlpatterns = [
    path('lectures/create/', teacher_views.create_lecture, name='create_lecture'),
    path('lectures/', teacher_views.lecture_list, name='lecture_list'),
   
    path('course_management/', teacher_views.course_management, name='course_management'),

 
    path('cv/', cv_views.cv_edit, name='cv_edit'),
    path('cv/password/', cv_views.password_2fa, name='password_2fa'),

]