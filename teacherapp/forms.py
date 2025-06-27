from django import forms
from core.models import Lecture

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'description', 'subject', 'video_url', 'pdf_file', 'slide_file']
