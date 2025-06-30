from django.urls import path
from . import views as teacher_views
from cv import views as cv_views

urlpatterns = [
<<<<<<< HEAD
    path('lectures/create/', views.create_lecture, name='create_lecture'),
    path('lectures/', views.lecture_list, name='lecture_list'),
    path('course/', views.lecture_list, name='course_list'),
    path('course_management/', views.course_management, name='course_management'),
]
=======
    path('lectures/create/', teacher_views.create_lecture, name='create_lecture'),
    path('lectures/', teacher_views.lecture_list, name='lecture_list'),
    path('cv/', cv_views.cv_edit, name='cv_edit'),
    path('cv/password/', cv_views.password_2fa, name='password_2fa'),
] 
>>>>>>> f2f91684fd9e1145cf58ad7f4c8989266fbe5b1e
