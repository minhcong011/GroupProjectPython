from django.urls import path
from . import views
from cv import views as cv_views

urlpatterns = [
<<<<<<< HEAD
    path('lectures/create/', teacher_views.create_lecture, name='create_lecture'),
    path('lectures/', teacher_views.lecture_list, name='lecture_list'),
    path('course/', teacher_views.lecture_list, name='course_list'),
    path('course_management/', teacher_views.course_management, name='course_management'),
    path('cv/', cv_views.cv_edit, name='cv_edit'),
    path('cv/password/', cv_views.password_2fa, name='password_2fa'),
]
=======
    path('lectures/create/', views.create_lecture, name='create_lecture'),
    path('lectures/', views.lecture_list, name='lecture_list'),
   
    path('course_management/', views.course_management, name='course_management'),

    path('cv/', cv_views.cv_edit, name='cv_edit'),
    path('cv/password/', cv_views.password_2fa, name='password_2fa'),

]
>>>>>>> 816dc9e8f4858b918fd7e9fa77b50a81041c6efe
