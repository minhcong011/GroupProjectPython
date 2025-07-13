from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from core.models import Account, Lecture, SystemLog
from teacherapp.models import Course, BaiTap, CauHoi, BaiLam, TestCase
from core.admin_site import admin_site

class Command(BaseCommand):
    help = 'Kiểm tra và sửa các vấn đề admin'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Bắt đầu kiểm tra admin system...")
        
        # 1. Kiểm tra models đã register
        self.check_registered_models()
        
        # 2. Kiểm tra URL patterns
        self.check_url_patterns()
        
        # 3. Kiểm tra database
        self.check_database()
        
        # 4. Tạo dữ liệu mẫu nếu cần
        self.create_sample_data()
        
        self.stdout.write(self.style.SUCCESS("✅ Hoàn thành kiểm tra admin system!"))

    def check_registered_models(self):
        """Kiểm tra các models đã được register"""
        self.stdout.write("\n📋 Kiểm tra models đã register:")
        
        expected_models = [
            'User', 'Group', 'Account', 'Lecture', 'SystemLog',
            'Course', 'BaiTap', 'CauHoi', 'BaiLam', 'TestCase'
        ]
        
        registered_models = [
            model.__name__ for model in admin_site._registry.keys()
        ]
        
        for model_name in expected_models:
            if model_name in registered_models:
                self.stdout.write(f"  ✓ {model_name}")
            else:
                self.stdout.write(f"  ✗ {model_name} - CHƯA REGISTER")

    def check_url_patterns(self):
        """Kiểm tra URL patterns"""
        from django.urls import reverse
        
        self.stdout.write("\n🔗 Kiểm tra URL patterns:")
        
        urls_to_check = [
            'custom_admin:index',
            'custom_admin:dashboard', 
            'custom_admin:backup_database',
            'custom_admin:restore_database',
            'custom_admin:system_stats',
        ]
        
        for url_name in urls_to_check:
            try:
                reverse(url_name)
                self.stdout.write(f"  ✓ {url_name}")
            except Exception as e:
                self.stdout.write(f"  ✗ {url_name}: {str(e)}")

    def check_database(self):
        """Kiểm tra kết nối database"""
        self.stdout.write("\n💾 Kiểm tra database:")
        
        models_to_check = [
            (User, 'Users'),
            (Account, 'Accounts'),
            (Course, 'Courses'),
            (BaiTap, 'Assignments'),
            (SystemLog, 'System Logs'),
        ]
        
        for model, name in models_to_check:
            try:
                count = model.objects.count()
                self.stdout.write(f"  ✓ {name}: {count} bản ghi")
            except Exception as e:
                self.stdout.write(f"  ✗ {name}: {str(e)}")

    def create_sample_data(self):
        """Tạo dữ liệu mẫu nếu cần"""
        self.stdout.write("\n🎯 Kiểm tra dữ liệu mẫu:")
        
        # Tạo superuser nếu chưa có
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write("  📝 Tạo superuser mặc định...")
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write("  ✅ Đã tạo superuser: admin/admin123")
        else:
            self.stdout.write("  ✓ Superuser đã tồn tại")
        
        # Tạo system log mẫu
        if SystemLog.objects.count() == 0:
            self.stdout.write("  📝 Tạo system log mẫu...")
            admin_user = User.objects.filter(is_superuser=True).first()
            if admin_user:
                SystemLog.objects.create(
                    user=admin_user,
                    action_type='SYSTEM_CHECK',
                    message='Kiểm tra hệ thống admin',
                    ip_address='127.0.0.1'
                )
                self.stdout.write("  ✅ Đã tạo system log mẫu")
        else:
            self.stdout.write("  ✓ System logs đã có dữ liệu")
