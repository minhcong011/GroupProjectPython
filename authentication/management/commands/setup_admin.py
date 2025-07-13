from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import SystemLog
from datetime import datetime


class Command(BaseCommand):
    help = 'Thiết lập hoàn chỉnh hệ thống admin'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Bắt đầu thiết lập hệ thống admin...\n')
        )
        
        # 1. Tạo tài khoản admin nếu chưa có
        username = 'admin'
        password = '123'
        email = 'admin@example.com'
        
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Đã tạo tài khoản admin: {username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Tài khoản admin đã tồn tại: {username}')
            )
        
        # 2. Tạo log khởi tạo hệ thống
        SystemLog.objects.create(
            user=None,
            action_type='SYSTEM',
            level='INFO',
            message='Hệ thống admin được thiết lập hoàn chỉnh',
            details={
                'admin_username': username,
                'setup_time': datetime.now().isoformat(),
                'features': [
                    'Dashboard với thống kê',
                    'Quản lý người dùng',
                    'Sao lưu & phục hồi database',
                    'Logs hệ thống tự động',
                    'Giao diện admin tùy chỉnh'
                ]
            }
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 THIẾT LẬP HOÀN THÀNH!\n'
                '================================\n'
                f'📋 Tài khoản Admin:\n'
                f'   - Username: {username}\n'
                f'   - Password: {password}\n'
                f'   - Email: {email}\n\n'
                f'🌐 Truy cập Admin:\n'
                f'   - URL: http://localhost:8000/admin/\n'
                f'   - Dashboard: http://localhost:8000/admin/dashboard/\n\n'
                f'⚡ Chức năng có sẵn:\n'
                f'   ✅ Dashboard với thống kê real-time\n'
                f'   ✅ Quản lý người dùng & phân quyền\n'
                f'   ✅ Quản lý khóa học & bài giảng\n'
                f'   ✅ Quản lý bài tập & câu hỏi\n'
                f'   ✅ Theo dõi bài làm học sinh\n'
                f'   ✅ Sao lưu & phục hồi database\n'
                f'   ✅ Logs hệ thống tự động\n'
                f'   ✅ Thống kê chi tiết\n\n'
                f'🛠️ Lệnh quản lý:\n'
                f'   - python manage.py backup_db\n'
                f'   - python manage.py restore_db <file>\n'
                f'   - python manage.py setup_admin\n'
            )
        )
