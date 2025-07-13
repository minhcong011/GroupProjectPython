from django.utils.deprecation import MiddlewareMixin
from core.models import SystemLog
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class AdminLogMiddleware(MiddlewareMixin):
    """Middleware để log các hoạt động admin"""
    
    def process_request(self, request):
        # Lưu thông tin request để sử dụng trong signals
        request._admin_log_data = {
            'ip_address': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


# Signal handlers
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    try:
        SystemLog.objects.create(
            user=user,
            action_type='LOGIN',
            message=f'Người dùng {user.username} đăng nhập thành công',
            ip_address=getattr(request, '_admin_log_data', {}).get('ip_address'),
            user_agent=getattr(request, '_admin_log_data', {}).get('user_agent', ''),
        )
    except:
        pass  # Tránh lỗi nếu database chưa được migrate


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    try:
        if user:
            SystemLog.objects.create(
                user=user,
                action_type='LOGOUT',
                message=f'Người dùng {user.username} đăng xuất',
                ip_address=getattr(request, '_admin_log_data', {}).get('ip_address'),
                user_agent=getattr(request, '_admin_log_data', {}).get('user_agent', ''),
            )
    except:
        pass
