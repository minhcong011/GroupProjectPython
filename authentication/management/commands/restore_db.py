from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Phục hồi database từ file backup'

    def add_arguments(self, parser):
        parser.add_argument(
            'backup_file',
            type=str,
            help='Đường dẫn file backup để phục hồi',
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Xác nhận phục hồi (sẽ xóa dữ liệu hiện tại)',
        )

    def handle(self, *args, **options):
        backup_file = options['backup_file']
        
        if not os.path.exists(backup_file):
            self.stdout.write(
                self.style.ERROR(f'File backup không tồn tại: {backup_file}')
            )
            return
        
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'CẢNH BÁO: Thao tác này sẽ xóa toàn bộ dữ liệu hiện tại!\n'
                    'Để xác nhận, chạy lại với --confirm'
                )
            )
            return
        
        try:
            # Flush database trước khi restore
            self.stdout.write('Đang xóa dữ liệu hiện tại...')
            call_command('flush', '--noinput')
            
            # Load dữ liệu từ backup
            self.stdout.write('Đang phục hồi dữ liệu...')
            call_command('loaddata', backup_file)
            
            self.stdout.write(
                self.style.SUCCESS(f'Phục hồi thành công từ: {backup_file}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Lỗi khi phục hồi: {str(e)}')
            )
