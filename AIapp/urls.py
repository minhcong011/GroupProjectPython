from django.urls import path
from . import views

app_name = 'AIapp'

urlpatterns = [
    path('ai/', views.ai_page, name='ai_page'),
    path('setup-guide/', views.setup_guide, name='setup_guide'),
    path('api/chat/', views.chat_api, name='chat_api'),
]
