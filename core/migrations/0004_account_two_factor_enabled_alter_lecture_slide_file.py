# Generated by Django 5.2.3 on 2025-06-30 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_lecture'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='two_factor_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='slide_file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/pdfs/'),
        ),
    ]
