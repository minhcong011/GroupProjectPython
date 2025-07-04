
from django import forms
from core.models import Lecture
from .models import BaiTap, CauHoi

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'description', 'subject', 'video_url', 'pdf_file', 'slide_file']


class BaiTapForm(forms.ModelForm):
    class Meta:
        model = BaiTap
        fields = ['tieu_de', 'mo_ta', 'loai_baitap', 'han_nop']

class CauHoiForm(forms.ModelForm):
    class Meta:
        model = CauHoi
        fields = ['noi_dung', 'lua_chon_a', 'lua_chon_b', 'lua_chon_c', 'lua_chon_d', 'dap_an_dung']

        
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
from django import forms
from .models import Course

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



