# Generated by Django 4.2.7 on 2025-06-27 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('company', models.CharField(blank=True, max_length=100)),
                ('title', models.CharField(blank=True, max_length=100)),
                ('timezone', models.CharField(blank=True, max_length=50)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
            ],
        ),
    ]
