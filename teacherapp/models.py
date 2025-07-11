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

class BaiLam(models.Model):
    """Bài làm của sinh viên"""
    sinh_vien = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bai_lam')
    bai_tap = models.ForeignKey(BaiTap, on_delete=models.CASCADE, related_name='bai_lam')
    thoi_gian_nop = models.DateTimeField(auto_now_add=True)
    diem_so = models.FloatField(null=True, blank=True)
    da_cham = models.BooleanField(default=False)
    
    # Cho bài trắc nghiệm
    dap_an_json = models.JSONField(null=True, blank=True)  # Lưu đáp án sinh viên chọn
    so_cau_dung = models.IntegerField(null=True, blank=True)  # Số câu trả lời đúng
    tong_so_cau = models.IntegerField(null=True, blank=True)  # Tổng số câu hỏi
    
    # Cho bài lập trình
    code_nop = models.TextField(null=True, blank=True)  # Code sinh viên nộp
    ket_qua_test = models.JSONField(null=True, blank=True)  # Kết quả chạy test
    so_test_pass = models.IntegerField(null=True, blank=True)  # Số test case pass
    tong_so_test = models.IntegerField(null=True, blank=True)  # Tổng số test case
    
    class Meta:
        unique_together = ['sinh_vien', 'bai_tap']
        verbose_name = 'Bài Làm'
        verbose_name_plural = 'Bài Làm'
    
    def __str__(self):
        return f"{self.sinh_vien.username} - {self.bai_tap.tieu_de}"

class TestCase(models.Model):
    """Test case cho bài lập trình"""
    bai_tap = models.ForeignKey(BaiTap, on_delete=models.CASCADE, related_name='test_cases')
    ten_test = models.CharField(max_length=100)
    input_data = models.TextField()  # Input cho test case
    expected_output = models.TextField()  # Output mong đợi
    diem_so = models.FloatField(default=1.0)  # Điểm cho test case này
    
    def __str__(self):
        return f"{self.bai_tap.tieu_de} - {self.ten_test}"

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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name

