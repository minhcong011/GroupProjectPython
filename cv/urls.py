# Đặt trong urls.py của app cv
from django.urls import path
from . import views

app_name = 'cv'

urlpatterns = [
    path('cv/', views.cv_edit, name='cv_edit'),
    # path('cvsv/', views.cvsv_edit, name='cvsv_edit'),  # Đường dẫn cho sinh viên
    path('cv/password/', views.password_2fa, name='password_2fa'),
]