from django.urls import path
from cv import views as cv_views
from . import views

urlpatterns = [
    path('lectures/create/', views.create_lecture, name='create_lecture'),
    path('lectures/', views.lecture_list, name='lecture_list'),
    path('course/', views.lecture_list, name='course_list'),
    path('course_management/', views.course_management, name='course_management'),
    path('cv/', cv_views.cv_edit, name='cv_edit'),
    path('cv/password/', cv_views.password_2fa, name='password_2fa'),
] 
