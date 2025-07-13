from django.contrib import admin
from .models import BaiTap, CauHoi, BaiLam, TestCase, Course
from core.admin_site import admin_site


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'status', 'start_date', 'end_date', 'participants', 'fee']
    list_filter = ['status', 'start_date', 'teacher']
    search_fields = ['name', 'teacher']
    ordering = ['-start_date']


@admin.register(BaiTap)
class BaiTapAdmin(admin.ModelAdmin):
    list_display = ['tieu_de', 'loai_baitap', 'nguoi_tao', 'han_nop', 'ngay_tao']
    list_filter = ['loai_baitap', 'ngay_tao', 'han_nop']
    search_fields = ['tieu_de', 'mo_ta']
    ordering = ['-ngay_tao']


@admin.register(CauHoi)
class CauHoiAdmin(admin.ModelAdmin):
    list_display = ['noi_dung', 'bai_tap', 'dap_an_dung']
    list_filter = ['bai_tap', 'dap_an_dung']
    search_fields = ['noi_dung']


@admin.register(BaiLam)
class BaiLamAdmin(admin.ModelAdmin):
    list_display = ['sinh_vien', 'bai_tap', 'thoi_gian_nop', 'diem_so', 'da_cham']
    list_filter = ['da_cham', 'thoi_gian_nop', 'bai_tap']
    search_fields = ['sinh_vien__username', 'bai_tap__tieu_de']
    ordering = ['-thoi_gian_nop']


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['bai_tap', 'ten_test', 'diem_so']
    list_filter = ['bai_tap']
    search_fields = ['ten_test', 'bai_tap__tieu_de']

# Đăng ký với custom admin site
admin_site.register(Course, CourseAdmin)
admin_site.register(BaiTap, BaiTapAdmin)
admin_site.register(CauHoi, CauHoiAdmin)
admin_site.register(BaiLam, BaiLamAdmin)
admin_site.register(TestCase, TestCaseAdmin)
