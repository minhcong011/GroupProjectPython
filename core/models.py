from django.db import models
from django.contrib.auth.models import User
from teacherapp.models import Course

class Account(models.Model):
    username = models.CharField(max_length=150, unique=True)
    is_teacher = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

# Thêm property để access Account từ User
def get_account(user_instance):
    try:
        return Account.objects.get(username=user_instance.username)
    except Account.DoesNotExist:
        return None

User.add_to_class('account', property(get_account))

class Lecture(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='uploads/pdfs/', blank=True, null=True)
    slide_file = models.FileField(upload_to='uploads/pdfs/', blank=True, null=True)
    subject = models.CharField(max_length=100, choices=[("Perl", "Perl"), ("Python", "Python")])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

class SystemLog(models.Model):
    LOG_LEVELS = [
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]
    
    ACTION_TYPES = [
        ('LOGIN', 'Đăng nhập'),
        ('LOGOUT', 'Đăng xuất'),
        ('CREATE', 'Tạo mới'),
        ('UPDATE', 'Cập nhật'),
        ('DELETE', 'Xóa'),
        ('VIEW', 'Xem'),
        ('BACKUP', 'Sao lưu'),
        ('RESTORE', 'Phục hồi'),
        ('SYSTEM', 'Hệ thống'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Người dùng")
    action_type = models.CharField("Loại hành động", max_length=20, choices=ACTION_TYPES)
    level = models.CharField("Mức độ", max_length=10, choices=LOG_LEVELS, default='INFO')
    message = models.TextField("Thông điệp")
    ip_address = models.GenericIPAddressField("Địa chỉ IP", null=True, blank=True)
    user_agent = models.TextField("User Agent", blank=True)
    timestamp = models.DateTimeField("Thời gian", auto_now_add=True)
    details = models.JSONField("Chi tiết", null=True, blank=True)
    
    class Meta:
        verbose_name = "Log Hệ thống"
        verbose_name_plural = "Logs Hệ thống"
        ordering = ['-timestamp']
    
    def __str__(self):
        user_info = self.user.username if self.user else "Anonymous"
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {user_info} - {self.get_action_type_display()}"