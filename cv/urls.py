from django.urls import path
from . import views

app_name = 'cv'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('cv/', views.cv_edit, name='cv_edit'),
    path('cv/password/', views.password_2fa, name='password_2fa'),
]
