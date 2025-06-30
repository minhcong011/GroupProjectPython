from django.urls import path
from . import views

app_name = 'studentapp'

urlpatterns = [
    path('bai-tap/', views.assignment_list, name='assignment_list'),
    path('ide-online/', views.ide_online, name='ide_online'),
    path('khoa-hoc/', views.khoa_hoc, name='khoa_hoc'),  
    path('chatbot/', views.chatbot, name='chatbot'), 
    path('nop-bai/', views.nop_bai, name='nop_bai'),
    path('cv/', views.cvsv_edit, name='cv_edit')
]