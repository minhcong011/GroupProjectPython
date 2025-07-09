from django.contrib import admin
from teacherapp.models import BaiTap, CauHoi, Course

# Tùy chỉnh Django Admin header
admin.site.site_header = "EduSync Admin Dashboard"
admin.site.site_title = "EduSync Admin"
admin.site.index_title = "Chào mừng đến với Admin Dashboard"

# Chỉ đăng ký các model từ teacherapp vì core models đã được đăng ký ở app core

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'status', 'start_date', 'end_date', 'participants', 'fee')
    list_filter = ('status', 'start_date', 'teacher')
    search_fields = ('name', 'teacher')
    date_hierarchy = 'start_date'
    fieldsets = (
        ('Thông tin khóa học', {
            'fields': ('name', 'teacher', 'status')
        }),
        ('Lịch trình', {
            'fields': ('start_date', 'end_date', 'schedule', 'sessions')
        }),
        ('Chi tiết', {
            'fields': ('curriculum', 'note', 'participants', 'fee')
        }),
        ('Quản lý', {
            'fields': ('created_by',)
        })
    )

# Inline cho CauHoi
class CauHoiInline(admin.TabularInline):
    model = CauHoi
    extra = 1
    fields = ('noi_dung', 'lua_chon_a', 'lua_chon_b', 'lua_chon_c', 'lua_chon_d', 'dap_an_dung')

@admin.register(BaiTap)
class BaiTapAdmin(admin.ModelAdmin):
    list_display = ('tieu_de', 'loai_baitap', 'nguoi_tao', 'han_nop', 'ngay_tao')
    list_filter = ('loai_baitap', 'han_nop', 'ngay_tao', 'nguoi_tao')
    search_fields = ('tieu_de', 'mo_ta')
    date_hierarchy = 'ngay_tao'
    readonly_fields = ('ngay_tao',)
    inlines = [CauHoiInline]
    
    fieldsets = (
        ('Thông tin bài tập', {
            'fields': ('tieu_de', 'mo_ta', 'loai_baitap')
        }),
        ('Thời gian', {
            'fields': ('han_nop', 'ngay_tao')
        }),
        ('Quản lý', {
            'fields': ('nguoi_tao',)
        })
    )

@admin.register(CauHoi)
class CauHoiAdmin(admin.ModelAdmin):
    list_display = ('noi_dung', 'bai_tap', 'dap_an_dung')
    list_filter = ('bai_tap', 'dap_an_dung')
    search_fields = ('noi_dung', 'bai_tap__tieu_de')
