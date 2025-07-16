from django.urls import path
from . import views

app_name = 'studentapp'

urlpatterns = [
    path('bai-tap/', views.assignment_list, name='assignment_list'),
    path('bai-tap/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('bai-tap/<int:assignment_id>/nop-quiz/', views.submit_quiz, name='submit_quiz'),
    path('bai-tap/<int:assignment_id>/nop-code/', views.submit_code_assignment, name='submit_code'),
    path('ide-online/', views.ide_online, name='ide_online'),
    path('run-code/', views.run_code, name='run_code'),
    path('chatbot/', views.chatbot, name='chatbot'), 
    path('nop-bai/', views.nop_bai, name='nop_bai'),
    path('course/', views.course, name='course'),
    path('course/<int:course_id>/lectures/', views.lecture_list, name='lecture_list'),
    path('api/courses/increment_participants/', views.increment_participants, name='increment_participants'),
]