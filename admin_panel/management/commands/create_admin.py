from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Tạo tài khoản admin mặc định với username: admin, password: 123'

    def handle(self, *args, **options):
        username = 'admin'
        password = '123'
        email = 'admin@perlpython.edu'
        
        # Kiểm tra xem tài khoản admin đã tồn tại chưa
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            # Cập nhật mật khẩu nếu tài khoản đã tồn tại
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            self.stdout.write(
                self.style.WARNING(f'Tài khoản admin đã tồn tại. Đã cập nhật mật khẩu thành "123"')
            )
        else:
            # Tạo tài khoản mới
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.is_staff = True
            user.is_superuser = True
            user.first_name = 'Admin'
            user.last_name = 'System'
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Đã tạo thành công tài khoản admin!')
            )
        
        self.stdout.write(
            self.style.SUCCESS('=' * 50)
        )
        self.stdout.write(
            self.style.SUCCESS('THÔNG TIN ĐĂNG NHẬP ADMIN:')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Username: {username}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Password: {password}')
        )
        self.stdout.write(
            self.style.SUCCESS('=' * 50)
        )
