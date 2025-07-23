
from django import forms
from core.models import Lecture
from .models import BaiTap, CauHoi, Course

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'description', 'subject', 'video_url', 'pdf_file', 'slide_file']


class BaiTapForm(forms.ModelForm):
    class Meta:
        model = BaiTap
        fields = ['khoa_hoc', 'tieu_de', 'mo_ta', 'loai_baitap', 'han_nop']
        widgets = {
            'khoa_hoc': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'tieu_de': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tiêu đề bài tập...'
            }),
            'mo_ta': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Mô tả chi tiết về bài tập...'
            }),
            'loai_baitap': forms.Select(attrs={
                'class': 'form-control'
            }),
            'han_nop': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            })
        }
        labels = {
            'khoa_hoc': 'Chọn khóa học',
            'tieu_de': 'Tiêu đề bài tập',
            'mo_ta': 'Mô tả',
            'loai_baitap': 'Loại bài tập',
            'han_nop': 'Hạn nộp'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Chỉ hiển thị các khóa học có sẵn
        self.fields['khoa_hoc'].queryset = Course.objects.all().order_by('name')
        self.fields['khoa_hoc'].empty_label = "-- Chọn khóa học --"

class CauHoiForm(forms.ModelForm):
    class Meta:
        model = CauHoi
        fields = ['noi_dung', 'lua_chon_a', 'lua_chon_b', 'lua_chon_c', 'lua_chon_d', 'dap_an_dung']
        widgets = {
            'noi_dung': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Nhập nội dung câu hỏi...'
            }),
            'lua_chon_a': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lựa chọn A...'
            }),
            'lua_chon_b': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lựa chọn B...'
            }),
            'lua_chon_c': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lựa chọn C...'
            }),
            'lua_chon_d': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lựa chọn D...'
            }),
            'dap_an_dung': forms.Select(attrs={
                'class': 'form-control'
            })
        }

        
from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
   class Meta:
        model = Course
        fields = '__all__'
        labels = {
            'name': 'Tên khóa học',
            'status': 'Trạng thái',
            'teacher': 'Giáo viên',
            'fee': 'Học phí',
            'start_date': 'Ngày bắt đầu',
            'end_date': 'Ngày kết thúc',
            'schedule': 'Lịch học',
            'sessions': 'Số buổi',
            'curriculum': 'Giáo trình',
            'note': 'Ghi chú',
            'participants': 'Số người tham gia',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Tên khóa học'}),
            'status': forms.TextInput(attrs={'class': 'input'}),
            'teacher': forms.TextInput(attrs={'class': 'input'}),
            'fee': forms.NumberInput(attrs={'class': 'input'}),
            'start_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'schedule': forms.TextInput(attrs={'class': 'input'}),
            'sessions': forms.NumberInput(attrs={'class': 'input'}),
            'curriculum': forms.TextInput(attrs={'class': 'input'}),
             'note': forms.Textarea(attrs={
                'rows': 4,'style': 'resize: vertical;'}),
            'participants': forms.NumberInput(attrs={'class': 'input'}),
        }

class CourseEditForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ['participants']  # ✅ Không cho chỉnh số lượng người tham gia
        labels = {
            'name': 'Tên khóa học',
            'status': 'Trạng thái',
            'teacher': 'Giáo viên',
            'fee': 'Học phí',
            'start_date': 'Ngày bắt đầu',
            'end_date': 'Ngày kết thúc',
            'schedule': 'Lịch học',
            'sessions': 'Số buổi',
            'curriculum': 'Giáo trình',
            'note': 'Ghi chú',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Tên khóa học'}),
            'status': forms.TextInput(attrs={'class': 'input'}),
            'teacher': forms.TextInput(attrs={'class': 'input'}),
            'fee': forms.NumberInput(attrs={'class': 'input'}),
            'start_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'schedule': forms.TextInput(attrs={'class': 'input'}),
            'sessions': forms.NumberInput(attrs={'class': 'input'}),
            'curriculum': forms.TextInput(attrs={'class': 'input'}),
            'note': forms.Textarea(attrs={'rows': 4, 'style': 'resize: vertical;'}),
        }



