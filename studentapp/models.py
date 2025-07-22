from django.db import models
from django.contrib.auth.models import User
from teacherapp.models import BaiTap, Course

# Create your models here.

class DanhGiaKhoaHoc(models.Model):
    LOAI_DANH_GIA_CHOICES = [
        ('khoa_hoc', 'Khóa học'),
        ('bai_tap', 'Bài tập'),
        ('giang_vien', 'Giảng viên'),
    ]
    
    SAO_CHOICES = [
        (1, '1 sao'),
        (2, '2 sao'),
        (3, '3 sao'),
        (4, '4 sao'),
        (5, '5 sao'),
    ]
    
    sinh_vien = models.ForeignKey(User, on_delete=models.CASCADE, related_name='danh_gia_sinh_vien')
    loai_danh_gia = models.CharField(max_length=20, choices=LOAI_DANH_GIA_CHOICES, default='khoa_hoc')
    khoa_hoc = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='danh_gia_khoa_hoc')
    bai_tap = models.ForeignKey(BaiTap, on_delete=models.CASCADE, null=True, blank=True, related_name='danh_gia_bai_tap')
    giang_vien = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='danh_gia_giang_vien')
    diem_sao = models.IntegerField(choices=SAO_CHOICES, default=5)
    tieu_de = models.CharField(max_length=200)
    noi_dung = models.TextField()
    gop_y = models.TextField(blank=True, null=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Đánh giá khóa học"
        verbose_name_plural = "Đánh giá khóa học"
        ordering = ['-ngay_tao']
    
    def __str__(self):
        return f"{self.sinh_vien.username} - {self.tieu_de} ({self.diem_sao} sao)"