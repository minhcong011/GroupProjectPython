# Đã xoá model Account khỏi app authentication, migration này giữ nguyên để đảm bảo lịch sử migration.
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Account',
        ),
    ]