from django.contrib import admin
from .models import Account, Lecture, SystemLog
from .admin_site import admin_site
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_teacher', 'is_email_verified', 'first_name', 'last_name', 'company']
    list_filter = ['is_teacher', 'is_email_verified', 'two_factor_enabled']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'company']
    ordering = ['username']
    readonly_fields = ['username']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('username', 'email', 'is_email_verified')
        }),
        ('Thông tin cá nhân', {
            'fields': ('first_name', 'last_name', 'phone_number', 'avatar')
        }),
        ('Thông tin công việc', {
            'fields': ('is_teacher', 'company', 'title', 'timezone')
        }),
        ('Bảo mật', {
            'fields': ('two_factor_enabled',)
        }),
    )


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created_by', 'course', 'created_at']
    list_filter = ['subject', 'course', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Thông tin bài giảng', {
            'fields': ('title', 'description', 'subject', 'course')
        }),
        ('Tài liệu', {
            'fields': ('video_url', 'pdf_file', 'slide_file')
        }),
        ('Thông tin tạo', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        }),
    )


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'action_type', 'level', 'message', 'ip_address']
    list_filter = ['action_type', 'level', 'timestamp']
    search_fields = ['user__username', 'message', 'ip_address']
    readonly_fields = ['timestamp', 'user', 'action_type', 'level', 'message', 'ip_address', 'user_agent', 'details']
    ordering = ['-timestamp']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False  # Không cho phép thêm log thủ công
    
    def has_change_permission(self, request, obj=None):
        return False  # Không cho phép sửa log
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Chỉ superuser mới được xóa log


# Đăng ký với custom admin site
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(Account, AccountAdmin)
admin_site.register(Lecture, LectureAdmin)
admin_site.register(SystemLog, SystemLogAdmin)
