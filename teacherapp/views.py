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

from django.shortcuts import render, redirect
from .models import Course
from .forms import CourseForm
from django.contrib.auth.decorators import login_required

@login_required
def course_management(request):
    courses = Course.objects.filter(created_by=request.user)
    form = CourseForm()
    return render(request, 'teacher_page/course_management.html', {'courses': courses, 'form': form})

def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user  # Gán người tạo là user hiện tại
            course.save()
            return redirect('course_management')
    return redirect('course_management')


from django.shortcuts import redirect, get_object_or_404
from .models import Course

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        course.delete()
        return redirect('course_management')
    return redirect('course_management')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Course
from .forms import CourseEditForm  

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = CourseEditForm(request.POST, instance=course)  
        if form.is_valid():
            updated = form.save(commit=False)
            updated.participants = course.participants  
            updated.created_by = request.user   # ⚠️ sửa đúng biến tên
            updated.save()
            print(">>> Đã lưu thành công")
            return redirect('course_management')
        else:
            print(">>> Form không hợp lệ:", form.errors)
    else:
        form = CourseEditForm(instance=course)

    return render(request, 'teacher_page/edit_course.html', {'form': form, 'course': course})

def khoa_hoc(request):
    courses = Course.objects.all().order_by('-id')  # mới nhất trước
    return render(request, 'studentapp/khoa_hoc.html', {'courses': courses})