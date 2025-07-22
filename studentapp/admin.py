from django.contrib import admin
from .models import DanhGiaKhoaHoc

# Register your models here.

@admin.register(DanhGiaKhoaHoc)
class DanhGiaKhoaHocAdmin(admin.ModelAdmin):
    list_display = ['tieu_de', 'sinh_vien', 'loai_danh_gia', 'get_doi_tuong_danh_gia', 'diem_sao', 'ngay_tao']
    list_filter = ['loai_danh_gia', 'diem_sao', 'ngay_tao']
    search_fields = ['tieu_de', 'sinh_vien__username', 'sinh_vien__first_name', 'sinh_vien__last_name']
    readonly_fields = ['ngay_tao', 'ngay_cap_nhat']
    list_per_page = 25
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('sinh_vien', 'loai_danh_gia', 'diem_sao')
        }),
        ('Đối tượng đánh giá', {
            'fields': ('khoa_hoc', 'bai_tap', 'giang_vien')
        }),
        ('Nội dung đánh giá', {
            'fields': ('tieu_de', 'noi_dung', 'gop_y')
        }),
        ('Thời gian', {
            'fields': ('ngay_tao', 'ngay_cap_nhat'),
            'classes': ('collapse',)
        }),
    )
    
    def get_doi_tuong_danh_gia(self, obj):
        if obj.khoa_hoc:
            return f"Khóa học: {obj.khoa_hoc.name}"
        elif obj.bai_tap:
            return f"Bài tập: {obj.bai_tap.tieu_de}"
        elif obj.giang_vien:
            if obj.giang_vien.first_name:
                return f"GV: {obj.giang_vien.first_name} {obj.giang_vien.last_name}"
            else:
                return f"GV: {obj.giang_vien.username}"
        return "Chưa xác định"
    
    get_doi_tuong_danh_gia.short_description = "Đối tượng đánh giá"
