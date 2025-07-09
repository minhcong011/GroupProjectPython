from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta

from core.models import Account, Lecture
from teacherapp.models import BaiTap, Course


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin để kiểm tra quyền admin"""
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class GuideView(TemplateView):
    template_name = 'admin_panel/guide.html'

class DashboardView(TemplateView):
    template_name = 'admin_panel/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Thống kê tổng quan
        context['total_courses'] = Course.objects.count()
        context['total_students'] = User.objects.filter(is_staff=False).count()
        context['total_assignments'] = BaiTap.objects.count()
        context['total_lectures'] = Lecture.objects.count()
        
        # Thống kê người dùng mới trong tuần
        week_ago = timezone.now() - timedelta(days=7)
        context['new_users_this_week'] = User.objects.filter(date_joined__gte=week_ago).count()
        
        # Bài tập gần đây
        context['recent_assignments'] = BaiTap.objects.order_by('-ngay_tao')[:5]
        
        # Khóa học đang hoạt động
        today = timezone.now().date()
        context['active_courses'] = Course.objects.filter(
            start_date__lte=today, 
            end_date__gte=today
        )[:5]
        
        # Hoạt động gần đây
        context['recent_lectures'] = Lecture.objects.order_by('-created_at')[:5]
        
        return context

# Quản lý khóa học
class CourseListView(AdminRequiredMixin, ListView):
    model = Course
    template_name = 'admin_panel/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

class CourseCreateView(AdminRequiredMixin, CreateView):
    model = Course
    template_name = 'admin_panel/course_form.html'
    fields = ['name', 'status', 'teacher', 'fee', 'start_date', 'end_date', 'schedule', 'sessions', 'curriculum', 'note', 'participants']
    success_url = reverse_lazy('admin_panel:course_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CourseUpdateView(AdminRequiredMixin, UpdateView):
    model = Course
    template_name = 'admin_panel/course_form.html'
    fields = ['name', 'status', 'teacher', 'fee', 'start_date', 'end_date', 'schedule', 'sessions', 'curriculum', 'note', 'participants']
    success_url = reverse_lazy('admin_panel:course_list')

class CourseDeleteView(AdminRequiredMixin, DeleteView):
    model = Course
    template_name = 'admin_panel/course_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:course_list')

# Quản lý bài tập
class AssignmentListView(AdminRequiredMixin, ListView):
    model = BaiTap
    template_name = 'admin_panel/assignment_list.html'
    context_object_name = 'assignments'
    paginate_by = 10

class AssignmentCreateView(AdminRequiredMixin, CreateView):
    model = BaiTap
    template_name = 'admin_panel/assignment_form.html'
    fields = ['tieu_de', 'mo_ta', 'loai_baitap', 'han_nop']
    success_url = reverse_lazy('admin_panel:assignment_list')
    
    def form_valid(self, form):
        form.instance.nguoi_tao = self.request.user
        return super().form_valid(form)

class AssignmentUpdateView(AdminRequiredMixin, UpdateView):
    model = BaiTap
    template_name = 'admin_panel/assignment_form.html'
    fields = ['tieu_de', 'mo_ta', 'loai_baitap', 'han_nop']
    success_url = reverse_lazy('admin_panel:assignment_list')

class AssignmentDeleteView(AdminRequiredMixin, DeleteView):
    model = BaiTap
    template_name = 'admin_panel/assignment_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:assignment_list')

# Quản lý người dùng
class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'admin_panel/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

class UserCreateView(AdminRequiredMixin, CreateView):
    model = User
    template_name = 'admin_panel/user_form.html'
    fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    success_url = reverse_lazy('admin_panel:user_list')

class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    template_name = 'admin_panel/user_form.html'
    fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    success_url = reverse_lazy('admin_panel:user_list')

# Quản lý bài giảng
class LectureListView(AdminRequiredMixin, ListView):
    model = Lecture
    template_name = 'admin_panel/lecture_list.html'
    context_object_name = 'lectures'
    paginate_by = 10

class LectureCreateView(AdminRequiredMixin, CreateView):
    model = Lecture
    template_name = 'admin_panel/lecture_form.html'
    fields = ['title', 'description', 'video_url', 'pdf_file', 'slide_file', 'subject']
    success_url = reverse_lazy('admin_panel:lecture_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class LectureUpdateView(AdminRequiredMixin, UpdateView):
    model = Lecture
    template_name = 'admin_panel/lecture_form.html'
    fields = ['title', 'description', 'video_url', 'pdf_file', 'slide_file', 'subject']
    success_url = reverse_lazy('admin_panel:lecture_list')

# Thống kê và báo cáo
class StatisticsView(AdminRequiredMixin, TemplateView):
    template_name = 'admin_panel/statistics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Thống kê theo tháng
        current_month = timezone.now().replace(day=1)
        last_month = (current_month - timedelta(days=1)).replace(day=1)
        
        context['courses_this_month'] = Course.objects.filter(start_date__gte=current_month).count()
        context['courses_last_month'] = Course.objects.filter(
            start_date__gte=last_month, 
            start_date__lt=current_month
        ).count()
        
        context['assignments_this_month'] = BaiTap.objects.filter(ngay_tao__gte=current_month).count()
        context['users_this_month'] = User.objects.filter(date_joined__gte=current_month).count()
        
        return context

class ReportsView(AdminRequiredMixin, TemplateView):
    template_name = 'admin_panel/reports.html'
