from django.urls import path
from . import views

app_name = 'studentapp'

urlpatterns = [
    path('bai-tap/', views.assignment_list, name='assignment_list'),
    path('bai-tap/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('bai-tap/<int:assignment_id>/nop-quiz/', views.submit_quiz, name='submit_quiz'),
    path('bai-tap/<int:assignment_id>/nop-code/', views.submit_code_assignment, name='submit_code'),
    path('ide-online/', views.ide_online, name='ide_online'),
    path('khoa-hoc/', views.khoa_hoc, name='khoa_hoc'),  
    path('chatbot/', views.chatbot, name='chatbot'), 
    path('nop-bai/', views.nop_bai, name='nop_bai'),
]