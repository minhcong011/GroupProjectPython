from django.urls import path
from . import views

urlpatterns = [
    path('api/get-groq-config/', views.get_groq_config, name='get_groq_config'),
]
