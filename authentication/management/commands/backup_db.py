from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
import os
from datetime import datetime


class Command(BaseCommand):
    help = 'Tạo backup database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            help='Đường dẫn file backup (tùy chọn)',
        )

    def handle(self, *args, **options):
        # Tạo tên file backup với timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if options['output']:
            backup_file = options['output']
        else:
            backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            backup_file = os.path.join(backup_dir, f'backup_{timestamp}.json')
        
        try:
            # Tạo backup bằng dumpdata
            with open(backup_file, 'w', encoding='utf-8') as f:
                call_command('dumpdata', 
                           '--natural-foreign', 
                           '--natural-primary', 
                           '--indent', '2',
                           stdout=f)
            
            self.stdout.write(
                self.style.SUCCESS(f'Backup thành công: {backup_file}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Lỗi khi backup: {str(e)}')
            )
