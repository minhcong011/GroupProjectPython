from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.urls import path
from django.contrib.auth.models import User
from core.models import SystemLog, Account, Lecture
from teacherapp.models import Course, BaiTap, BaiLam
from django.db.models import Count, Q
from datetime import datetime, timedelta


class CustomAdminSite(AdminSite):
    site_header = "Hệ thống Quản trị Giáo dục"
    site_title = "Admin Portal"
    index_title = "Bảng điều khiển quản trị"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
            path('backup/', self.admin_view(self.backup_view), name='backup_database'),
            path('restore/', self.admin_view(self.restore_view), name='restore_database'),
            path('system-stats/', self.admin_view(self.system_stats_view), name='system_stats'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        """Dashboard tùy chỉnh với thống kê"""
        context = self.get_dashboard_context(request)
        return TemplateResponse(request, 'admin/dashboard.html', context)
    
    def get_dashboard_context(self, request):
        """Lấy dữ liệu thống kê cho dashboard"""
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Thống kê người dùng
        total_users = User.objects.count()
        teachers = Account.objects.filter(is_teacher=True).count()
        students = total_users - teachers
        new_users_week = User.objects.filter(date_joined__gte=week_ago).count()
        
        # Thống kê khóa học
        total_courses = Course.objects.count()
        active_courses = Course.objects.filter(status='active').count()
        
        # Thống kê bài tập
        total_assignments = BaiTap.objects.count()
        submissions_today = BaiLam.objects.filter(thoi_gian_nop__date=today).count()
        pending_grading = BaiLam.objects.filter(da_cham=False).count()
        
        # Thống kê bài giảng
        total_lectures = Lecture.objects.count()
        
        # Hoạt động gần đây
        recent_logs = SystemLog.objects.select_related('user').order_by('-timestamp')[:10]
        
        # Thống kê theo ngày (7 ngày gần nhất)
        daily_stats = []
        for i in range(7):
            date = today - timedelta(days=i)
            logins = SystemLog.objects.filter(
                action_type='LOGIN',
                timestamp__date=date
            ).count()
            submissions = BaiLam.objects.filter(
                thoi_gian_nop__date=date
            ).count()
            daily_stats.append({
                'date': date.strftime('%d/%m'),
                'logins': logins,
                'submissions': submissions
            })
        
        return {
            'title': 'Dashboard',
            'stats': {
                'total_users': total_users,
                'teachers': teachers,
                'students': students,
                'new_users_week': new_users_week,
                'total_courses': total_courses,
                'active_courses': active_courses,
                'total_assignments': total_assignments,
                'submissions_today': submissions_today,
                'pending_grading': pending_grading,
                'total_lectures': total_lectures,
            },
            'recent_logs': recent_logs,
            'daily_stats': list(reversed(daily_stats)),
        }
    
    def backup_view(self, request):
        """View để backup database"""
        from django.contrib import messages
        from django.shortcuts import redirect
        from django.core.management import call_command
        import os
        
        if request.method == 'POST':
            try:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_dir = 'backups'
                os.makedirs(backup_dir, exist_ok=True)
                backup_file = os.path.join(backup_dir, f'backup_{timestamp}.json')
                
                call_command('backup_db', output=backup_file)
                
                # Log the action
                SystemLog.objects.create(
                    user=request.user,
                    action_type='BACKUP',
                    message=f'Tạo backup database: {backup_file}',
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
                messages.success(request, f'Backup thành công: {backup_file}')
            except Exception as e:
                messages.error(request, f'Lỗi khi backup: {str(e)}')
            
            return redirect('admin:index')
        
        return TemplateResponse(request, 'admin/backup_confirm.html', {
            'title': 'Sao lưu Database',
        })
    
    def restore_view(self, request):
        """View để restore database"""
        from django.contrib import messages
        from django.shortcuts import redirect
        from django.core.management import call_command
        import os
        
        if request.method == 'POST':
            backup_file = request.POST.get('backup_file')
            if backup_file and os.path.exists(backup_file):
                try:
                    call_command('restore_db', backup_file, confirm=True)
                    
                    # Log the action
                    SystemLog.objects.create(
                        user=request.user,
                        action_type='RESTORE',
                        message=f'Phục hồi database từ: {backup_file}',
                        ip_address=request.META.get('REMOTE_ADDR'),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
                    
                    messages.success(request, f'Phục hồi thành công từ: {backup_file}')
                except Exception as e:
                    messages.error(request, f'Lỗi khi phục hồi: {str(e)}')
            else:
                messages.error(request, 'File backup không tồn tại!')
            
            return redirect('admin:index')
        
        # List available backup files
        backup_dir = 'backups'
        backup_files = []
        if os.path.exists(backup_dir):
            for f in os.listdir(backup_dir):
                if f.endswith('.json'):
                    file_path = os.path.join(backup_dir, f)
                    file_stat = os.stat(file_path)
                    backup_files.append({
                        'path': file_path,
                        'name': f,
                        'size': file_stat.st_size,
                        'modified': datetime.fromtimestamp(file_stat.st_mtime)
                    })
        
        backup_files.sort(key=lambda x: x['modified'], reverse=True)
        
        return TemplateResponse(request, 'admin/restore_confirm.html', {
            'title': 'Phục hồi Database',
            'backup_files': backup_files,
        })
    
    def system_stats_view(self, request):
        """View thống kê hệ thống chi tiết"""
        context = self.get_system_stats_context(request)
        return TemplateResponse(request, 'admin/system_stats.html', context)
    
    def get_system_stats_context(self, request):
        """Lấy thống kê hệ thống chi tiết"""
        # Thống kê logs theo loại
        log_stats = SystemLog.objects.values('action_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Thống kê người dùng hoạt động
        active_users = SystemLog.objects.filter(
            timestamp__gte=datetime.now() - timedelta(days=30)
        ).values('user__username').annotate(
            login_count=Count('id', filter=Q(action_type='LOGIN'))
        ).order_by('-login_count')[:10]
        
        # Thống kê bài tập theo tháng
        monthly_assignments = BaiTap.objects.filter(
            ngay_tao__gte=datetime.now() - timedelta(days=90)
        ).extra(
            select={'month': "strftime('%%Y-%%m', ngay_tao)"}
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        return {
            'title': 'Thống kê Hệ thống',
            'log_stats': log_stats,
            'active_users': active_users,
            'monthly_assignments': monthly_assignments,
        }


# Khởi tạo custom admin site
admin_site = CustomAdminSite(name='custom_admin')
