#!/usr/bin/env python
"""
Script kiểm tra và sửa các lỗi admin
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Main.settings')
django.setup()

def check_templates():
    """Kiểm tra template syntax"""
    from django.template import loader, Context, TemplateSyntaxError
    
    templates = [
        'admin/index.html',
        'admin/dashboard.html', 
        'admin/backup_confirm.html',
        'admin/restore_confirm.html',
        'admin/system_stats.html'
    ]
    
    print("=== KIỂM TRA TEMPLATE SYNTAX ===")
    for template_name in templates:
        try:
            template = loader.get_template(template_name)
            # Try rendering with empty context
            template.render(Context({}))
            print(f"✓ {template_name}: OK")
        except TemplateSyntaxError as e:
            print(f"✗ {template_name}: {str(e)}")
        except Exception as e:
            print(f"⚠ {template_name}: {str(e)}")

def check_models():
    """Kiểm tra models có hoạt động không"""
    from django.contrib.auth.models import User, Group
    from core.models import Account, Lecture, SystemLog
    from teacherapp.models import Course, BaiTap, CauHoi, BaiLam, TestCase
    
    print("\n=== KIỂM TRA MODELS ===")
    models = [
        (User, 'User'),
        (Group, 'Group'),
        (Account, 'Account'),
        (Lecture, 'Lecture'),
        (SystemLog, 'SystemLog'),
        (Course, 'Course'),
        (BaiTap, 'BaiTap'),
        (CauHoi, 'CauHoi'),
        (BaiLam, 'BaiLam'),
        (TestCase, 'TestCase'),
    ]
    
    for model, name in models:
        try:
            count = model.objects.count()
            print(f"✓ {name}: {count} records")
        except Exception as e:
            print(f"✗ {name}: {str(e)}")

def check_admin_views():
    """Kiểm tra admin views"""
    from core.admin_site import admin_site
    from django.test import RequestFactory
    from django.contrib.auth.models import AnonymousUser
    
    print("\n=== KIỂM TRA ADMIN VIEWS ===")
    
    factory = RequestFactory()
    request = factory.get('/admin/')
    request.user = AnonymousUser()
    
    try:
        # Test dashboard view
        response = admin_site.dashboard_view(request)
        print(f"✓ dashboard_view: {response.status_code}")
    except Exception as e:
        print(f"✗ dashboard_view: {str(e)}")
    
    try:
        # Test system stats view  
        response = admin_site.system_stats_view(request)
        print(f"✓ system_stats_view: {response.status_code}")
    except Exception as e:
        print(f"✗ system_stats_view: {str(e)}")

if __name__ == "__main__":
    check_templates()
    check_models()
    check_admin_views()
