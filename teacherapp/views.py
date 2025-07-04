# Sửa câu hỏi
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LectureForm, BaiTapForm, CauHoiForm, CourseForm, CourseEditForm
from .models import BaiTap, CauHoi, Course
from django.http import HttpResponseForbidden
from core.models import Lecture
from django.contrib import messages

@login_required
def edit_question(request, question_id):
    question = get_object_or_404(CauHoi, id=question_id, bai_tap__nguoi_tao=request.user)
    if request.method == 'POST':
        form = CauHoiForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã cập nhật câu hỏi thành công!')
            return redirect('edit_assignment', assignment_id=question.bai_tap.id)
    else:
        form = CauHoiForm(instance=question)
    return render(request, 'teacher_page/edit_question.html', {'form': form, 'question': question})

# Xóa câu hỏi
@login_required
def delete_question(request, question_id):
    question = get_object_or_404(CauHoi, id=question_id, bai_tap__nguoi_tao=request.user)
    assignment_id = question.bai_tap.id
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Đã xóa câu hỏi thành công!')
        return redirect('edit_assignment', assignment_id=assignment_id)
    return render(request, 'teacher_page/delete_question_confirm.html', {'question': question})



@login_required
def delete_assignment(request, assignment_id):
    try:
        baitap = BaiTap.objects.get(id=assignment_id, nguoi_tao=request.user)
    except BaiTap.DoesNotExist:
        return HttpResponseForbidden()
    if request.method == 'POST':
        baitap.delete()
        return redirect('assignment_list')
    return render(request, 'teacher_page/delete_assignment_confirm.html', {'assignment': baitap})

@login_required
def assignment_list(request):
    assignments = BaiTap.objects.filter(nguoi_tao=request.user)
    from core.models import Lecture
    lectures = Lecture.objects.filter(created_by=request.user)
    return render(request, 'teacher_page/assignment_list.html', {'assignments': assignments, 'lectures': lectures})


@login_required
def create_assignment(request):
    if request.method == 'POST':
        form = BaiTapForm(request.POST)
        if form.is_valid():
            baitap = form.save(commit=False)
            baitap.nguoi_tao = request.user
            baitap.save()
            if baitap.loai_baitap == 'quiz':
                return redirect('add_questions', assignment_id=baitap.id)
            return redirect('assignment_list')
    else:
        form = BaiTapForm()
    return render(request, 'teacher_page/create_assignment.html', {'form': form})


@login_required
def add_questions(request, assignment_id):
    baitap = BaiTap.objects.get(id=assignment_id, nguoi_tao=request.user)
    if request.method == 'POST':
        form = CauHoiForm(request.POST)
        if form.is_valid():
            cauhoi = form.save(commit=False)
            cauhoi.bai_tap = baitap
            cauhoi.save()
            if 'add_another' in request.POST:
                return redirect('add_questions', assignment_id=baitap.id)
            return redirect('assignment_list')
    else:
        form = CauHoiForm()
    return render(request, 'teacher_page/add_questions.html', {'form': form, 'assignment': baitap})

# Create your views here.

# Sửa bài tập
from django.shortcuts import get_object_or_404
@login_required
def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(BaiTap, id=assignment_id, nguoi_tao=request.user)
    if request.method == 'POST':
        form = BaiTapForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã cập nhật bài tập thành công!')
            return redirect('assignment_list')
    else:
        form = BaiTapForm(instance=assignment)
    return render(request, 'teacher_page/edit_assignment.html', {'form': form, 'assignment': assignment})
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


# Xem chi tiết bài giảng (đề cương)
@login_required
def lecture_detail(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk, created_by=request.user)
    return render(request, 'teacher_page/lecture_detail.html', {'lecture': lecture})

# Chỉnh sửa bài giảng (đề cương)
@login_required
def edit_lecture(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = LectureForm(request.POST, request.FILES, instance=lecture)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã cập nhật đề cương thành công!')
            return redirect('lecture_list')
    else:
        form = LectureForm(instance=lecture)
    return render(request, 'teacher_page/edit_lecture.html', {'form': form, 'lecture': lecture})

# Xóa bài giảng (đề cương)
@login_required
def delete_lecture(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk, created_by=request.user)
    if request.method == 'POST':
        lecture.delete()
        messages.success(request, 'Đã xóa đề cương thành công!')
        return redirect('lecture_list')
    return render(request, 'teacher_page/delete_lecture_confirm.html', {'lecture': lecture})

@login_required
def lecture_list(request):
    lectures = Lecture.objects.filter(created_by=request.user)
    return render(request, 'teacher_page/lecture_list.html', {'lectures': lectures})

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
            course.created_by = request.user  
            course.save()
            return redirect('course_management')
    return redirect('course_management')

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == "POST":
        course.delete()
        return redirect('course_management')
    return redirect('course_management')

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = CourseEditForm(request.POST, instance=course)  
        if form.is_valid():
            updated = form.save(commit=False)
            updated.participants = course.participants  
            updated.created_by = request.user
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