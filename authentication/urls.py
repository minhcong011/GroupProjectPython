# authentication/urls.py
from django.urls import path
from authentication import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('teacher/', views.teacher_home, name='teacher_home'),   
    path('student/', views.student_home, name='student_home'),   
]