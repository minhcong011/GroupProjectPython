from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Dashboard chính
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('guide/', views.GuideView.as_view(), name='guide'),
    
    # Quản lý khóa học
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/add/', views.CourseCreateView.as_view(), name='course_add'),
    path('courses/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    
    # Quản lý bài tập
    path('assignments/', views.AssignmentListView.as_view(), name='assignment_list'),
    path('assignments/add/', views.AssignmentCreateView.as_view(), name='assignment_add'),
    path('assignments/<int:pk>/edit/', views.AssignmentUpdateView.as_view(), name='assignment_edit'),
    path('assignments/<int:pk>/delete/', views.AssignmentDeleteView.as_view(), name='assignment_delete'),
    
    # Quản lý người dùng
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/add/', views.UserCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    
    # Quản lý bài giảng
    path('lectures/', views.LectureListView.as_view(), name='lecture_list'),
    path('lectures/add/', views.LectureCreateView.as_view(), name='lecture_add'),
    path('lectures/<int:pk>/edit/', views.LectureUpdateView.as_view(), name='lecture_edit'),
    
    # Thống kê và báo cáo
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
]
