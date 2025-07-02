

from django.db import models
from django.contrib.auth.models import User




class BaiTap(models.Model):
    LOAI_BAITAP_CHOICES = [
        ('code', 'Lập trình (Python/Perl)'),
        ('quiz', 'Trắc nghiệm'),
    ]
    tieu_de = models.CharField("Tiêu đề", max_length=255)
    mo_ta = models.TextField("Mô tả")
    loai_baitap = models.CharField("Loại bài tập", max_length=10, choices=LOAI_BAITAP_CHOICES)
    han_nop = models.DateTimeField("Hạn nộp")
    nguoi_tao = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người tạo")
    ngay_tao = models.DateTimeField("Ngày tạo", auto_now_add=True)

    def __str__(self):
        return self.tieu_de

   
   


class CauHoi(models.Model):
    bai_tap = models.ForeignKey(BaiTap, on_delete=models.CASCADE, related_name='cau_hoi', verbose_name="Bài tập")
    noi_dung = models.TextField("Nội dung câu hỏi")
    lua_chon_a = models.CharField("Lựa chọn A", max_length=255, blank=True)
    lua_chon_b = models.CharField("Lựa chọn B", max_length=255, blank=True)
    lua_chon_c = models.CharField("Lựa chọn C", max_length=255, blank=True)
    lua_chon_d = models.CharField("Lựa chọn D", max_length=255, blank=True)
    dap_an_dung = models.CharField("Đáp án đúng", max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')], blank=True)

    def __str__(self):
        return self.noi_dung

class Course(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    teacher = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    schedule = models.CharField(max_length=200)
    sessions = models.IntegerField(default=0)  # Tổng số buổi
    curriculum = models.TextField(blank=True)
    note = models.TextField(blank=True)
    participants = models.IntegerField(default=0)

    def __str__(self):
        return self.name


