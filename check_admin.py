#!/usr/bin/env python
"""
Script kiểm tra admin site và debug các vấn đề
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Main.settings')
django.setup()

def test_admin_urls():
    """Test các URL patterns của admin"""
    from django.urls import reverse
    from core.admin_site import admin_site
    
    print("=== KIỂM TRA ADMIN URLS ===")
    
    # Test các URL custom
    custom_urls = [
        'custom_admin:dashboard',
        'custom_admin:backup_database',
        'custom_admin:restore_database',
        'custom_admin:system_stats',
        'custom_admin:index',
    ]
    
    for url_name in custom_urls:
        try:
            url = reverse(url_name)
            print(f"✓ {url_name}: {url}")
        except Exception as e:
            print(f"✗ {url_name}: {str(e)}")
    
    # Test các URL model changelist
    model_urls = [
        'custom_admin:auth_user_changelist',
        'custom_admin:core_account_changelist', 
        'custom_admin:auth_group_changelist',
        'custom_admin:teacherapp_course_changelist',
        'custom_admin:core_lecture_changelist',
        'custom_admin:teacherapp_baitap_changelist',
        'custom_admin:teacherapp_cauhoi_changelist',
        'custom_admin:teacherapp_bailam_changelist',
        'custom_admin:core_systemlog_changelist',
        'custom_admin:teacherapp_testcase_changelist',
    ]
    
    print("\n=== KIỂM TRA MODEL URLS ===")
    for url_name in model_urls:
        try:
            url = reverse(url_name)
            print(f"✓ {url_name}: {url}")
        except Exception as e:
            print(f"✗ {url_name}: {str(e)}")

def test_registered_models():
    """Kiểm tra các models đã được register"""
    from core.admin_site import admin_site
    
    print("\n=== MODELS ĐÃ REGISTER ===")
    for model, admin_class in admin_site._registry.items():
        print(f"✓ {model._meta.app_label}.{model.__name__}: {admin_class.__class__.__name__}")

if __name__ == "__main__":
    test_admin_urls()
    test_registered_models()
