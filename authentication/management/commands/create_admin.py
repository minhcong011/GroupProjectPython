from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Tạo tài khoản admin cố định'

    def handle(self, *args, **options):
        username = 'admin'
        password = '123'
        email = 'admin@example.com'
        
        # Kiểm tra xem tài khoản admin đã tồn tại chưa
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Tài khoản admin "{username}" đã tồn tại!')
            )
            return
        
        # Tạo tài khoản superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Đã tạo thành công tài khoản admin!\n'
                f'Username: {username}\n'
                f'Password: {password}\n'
                f'Email: {email}'
            )
        )
