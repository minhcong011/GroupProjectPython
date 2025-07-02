
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
