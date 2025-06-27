from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LectureForm
from core.models import Lecture
from django.contrib import messages
# Create your views here.
@login_required
def create_lecture(request):
    if request.method == 'POST':
        form = LectureForm(request.POST, request.FILES)
        if form.is_valid():
            print('faskdjfhs')
            lecture = form.save(commit=False)
            lecture.created_by = request.user
            lecture.save()
            messages.success(request, 'Bài giảng đã được tạo thành công!')
            return redirect('lecture_list')
    else:
        form = LectureForm()
    return render(request, 'teacher_page/create_lecture.html', {'form': form})

@login_required
def lecture_list(request):
    lectures = Lecture.objects.filter(created_by=request.user)
    return render(request, 'teacher_page/lecture_list.html', {'lectures': lectures})