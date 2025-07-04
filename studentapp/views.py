from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from teacherapp.models import Course, BaiTap, CauHoi

def assignment_list(request):
    assignments = BaiTap.objects.all().order_by('-ngay_tao')
    return render(request, "student_page/assignment_list.html", {"assignments": assignments})

def ide_online(request):
    return render(request, "student_page/IDE_Onl.html")

def khoa_hoc(request):
    courses = Course.objects.all()  # Lấy tất cả các khóa học do giáo viên tạo
    return render(request, "student_page/Khoa_hoc.html", {"courses": courses}) 

def chatbot(request):
    return render(request, "student_page/Chat_bot.html")

def nop_bai(request):
    context = {}
    if request.method == "POST":
        if 'code' in request.POST:
            
            code = request.POST.get('code')
            language = request.POST.get('language')
            
            context['message'] = "Đã nhận code. (Chưa xử lý lưu/chấm thực tế)"
        elif 'file' in request.FILES:
            
            file = request.FILES['file']
            
            context['submitted_file'] = {
                'name': file.name,
                'time': timezone.now()
            }
            context['message'] = "Đã nhận file. (Chưa xử lý lưu thực tế)"
    return render(request, "student_page/nop_bai.html", context)
def cvsv_edit(request):
    # Nếu sau này có phân quyền, kiểm tra user là sinh viên hay giáo viên ở đây
    return render(request, "cv/cv_student.html")

@login_required
def assignment_detail(request, assignment_id):
    """View để sinh viên xem chi tiết bài tập và làm bài"""
    assignment = get_object_or_404(BaiTap, id=assignment_id)
    
    # Kiểm tra loại bài tập
    if assignment.loai_baitap == 'code':
        # Nếu là bài tập code, chuyển hướng đến IDE online với thông tin bài tập
        return render(request, "student_page/IDE_Onl.html", {
            'assignment': assignment,
            'assignment_mode': True
        })
    elif assignment.loai_baitap == 'quiz':
        # Nếu là bài tập trắc nghiệm, lấy các câu hỏi và hiển thị form quiz
        questions = CauHoi.objects.filter(bai_tap=assignment)
        return render(request, "student_page/quiz_assignment.html", {
            'assignment': assignment,
            'questions': questions
        })
    
    return render(request, "student_page/assignment_detail.html", {'assignment': assignment})

@login_required
def submit_quiz(request, assignment_id):
    """View để sinh viên nộp bài trắc nghiệm"""
    assignment = get_object_or_404(BaiTap, id=assignment_id)
    
    if request.method == 'POST':
        questions = CauHoi.objects.filter(bai_tap=assignment)
        score = 0
        total_questions = questions.count()
        results = []
        
        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')
            is_correct = user_answer == question.dap_an_dung
            if is_correct:
                score += 1
            
            results.append({
                'question': question,
                'user_answer': user_answer,
                'correct_answer': question.dap_an_dung,
                'is_correct': is_correct
            })
        
        # Tính phần trăm điểm
        percentage = (score / total_questions * 100) if total_questions > 0 else 0
        
        context = {
            'assignment': assignment,
            'results': results,
            'score': score,
            'total_questions': total_questions,
            'percentage': percentage
        }
        
        messages.success(request, f'Đã nộp bài thành công! Điểm của bạn: {score}/{total_questions} ({percentage:.1f}%)')
        return render(request, "student_page/quiz_result.html", context)
    
    return redirect('studentapp:assignment_detail', assignment_id=assignment_id)

@login_required
def submit_code_assignment(request, assignment_id):
    """View để sinh viên nộp bài code"""
    assignment = get_object_or_404(BaiTap, id=assignment_id)
    
    if request.method == 'POST':
        code = request.POST.get('code', '')
        language = request.POST.get('language', 'python')
        
        # Ở đây bạn có thể lưu code vào database hoặc xử lý thêm
        # Tạm thời chỉ hiển thị thông báo thành công
        
        context = {
            'assignment': assignment,
            'submitted_code': code,
            'language': language,
            'submission_time': timezone.now()
        }
        
        messages.success(request, 'Đã nộp bài code thành công!')
        return render(request, "student_page/code_submission_result.html", context)
    
    return redirect('studentapp:assignment_detail', assignment_id=assignment_id)
