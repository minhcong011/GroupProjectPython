from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from teacherapp.models import Course, BaiTap, CauHoi

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import subprocess
import json
import tempfile
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


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
        
        # Lưu đáp án sinh viên
        dap_an_sinh_vien = {}
        
        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')
            dap_an_sinh_vien[str(question.id)] = user_answer
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
        
        # Lưu bài làm vào database
        from teacherapp.models import BaiLam
        bai_lam, created = BaiLam.objects.get_or_create(
            sinh_vien=request.user,
            bai_tap=assignment,
            defaults={
                'dap_an_json': dap_an_sinh_vien,
                'diem_so': round((score / total_questions) * 10, 2) if total_questions > 0 else 0,
                'da_cham': True  # Tự động chấm bài trắc nghiệm
            }
        )
        
        if not created:
            # Cập nhật bài làm nếu đã tồn tại
            bai_lam.dap_an_json = dap_an_sinh_vien
            bai_lam.diem_so = round((score / total_questions) * 10, 2) if total_questions > 0 else 0
            bai_lam.da_cham = True
            bai_lam.save()
        
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
        
        # Lưu bài làm vào database
        from teacherapp.models import BaiLam
        bai_lam, created = BaiLam.objects.get_or_create(
            sinh_vien=request.user,
            bai_tap=assignment,
            defaults={
                'code_nop': code,
                'da_cham': False  # Cần giáo viên chấm thủ công
            }
        )
        
        if not created:
            # Cập nhật bài làm nếu đã tồn tại
            bai_lam.code_nop = code
            bai_lam.da_cham = False
            bai_lam.save()
        
        context = {
            'assignment': assignment,
            'submitted_code': code,
            'language': language,
            'submission_time': timezone.now()
        }
        
        messages.success(request, 'Đã nộp bài code thành công!')
        return render(request, "student_page/code_submission_result.html", context)
    
    return redirect('studentapp:assignment_detail', assignment_id=assignment_id)



def course(request):
    courses = Course.objects.all().order_by('-id')
    return render(request, "student_page/course.html", {"courses": courses})


@csrf_exempt
@require_POST
def increment_participants(request):
    course_id = request.GET.get('id')
    if not course_id:
        return JsonResponse({'success': False, 'error': 'Missing course id'})
    try:
        course = Course.objects.get(id=course_id)
        course.participants += 1
        course.save()
        return JsonResponse({'success': True, 'participants': course.participants})
    except Course.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Course not found'})

@csrf_exempt
@require_http_methods(["POST"])
def run_code(request):
    """
    Chạy code Python/Perl bằng subprocess
    """
    try:
        data = json.loads(request.body)
        code = data.get('code', '')
        language = data.get('language', 'python')
        
        # Validate input
        if not code.strip():
            return JsonResponse({
                'output': 'Lỗi: Không có code để chạy!',
                'success': False
            })
        
        # Giới hạn độ dài code để tránh spam
        if len(code) > 10000:  # 10KB
            return JsonResponse({
                'output': 'Lỗi: Code quá dài (tối đa 10.000 ký tự)',
                'success': False
            })
        
        # Kiểm tra các lệnh nguy hiểm
        dangerous_keywords = [
            'import os', 'import sys', 'import subprocess', 'import shutil',
            'open(', 'file(', 'exec(', 'eval(', '__import__',
            'rm ', 'del ', 'format', 'remove'
        ]
        
        code_lower = code.lower()
        for keyword in dangerous_keywords:
            if keyword in code_lower:
                return JsonResponse({
                    'output': f'Lỗi bảo mật: Không được sử dụng "{keyword}" trong code',
                    'success': False
                })
        
        # Tạo file tạm để lưu code
        if language == 'python':
            file_extension = '.py'
            # Thêm encoding UTF-8 và xử lý output cho Python
            code_with_encoding = f'''# -*- coding: utf-8 -*-
import sys
import io
import os

# Thiết lập encoding UTF-8 cho output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
elif hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Thiết lập môi trường UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Code của người dùng
{code}
'''
        elif language == 'perl':
            file_extension = '.pl'
            code_with_encoding = f'''use utf8;
use open qw(:std :utf8);
binmode(STDOUT, ":utf8");
binmode(STDERR, ":utf8");

# Code của người dùng
{code}
'''
        else:
            return JsonResponse({
                'output': 'Lỗi: Ngôn ngữ không được hỗ trợ',
                'success': False
            })
        
        # Tạo file tạm thời
        with tempfile.NamedTemporaryFile(mode='w', suffix=file_extension, delete=False, encoding='utf-8') as temp_file:
            temp_file.write(code_with_encoding)
            temp_file_path = temp_file.name
        
        try:
            # Thiết lập môi trường UTF-8
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONUTF8'] = '1'
            env['LC_ALL'] = 'C.UTF-8'
            
            # Chạy code với subprocess
            if language == 'python':
                # Chạy Python với encoding UTF-8
                result = subprocess.run(
                    ['python', '-X', 'utf8', temp_file_path],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=tempfile.gettempdir(),
                    encoding='utf-8',
                    errors='replace',  # Thay thế ký tự lỗi thay vì crash
                    env=env
                )
            else:
                # Chạy Perl
                result = subprocess.run(
                    ['perl', temp_file_path],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=tempfile.gettempdir(),
                    encoding='utf-8',
                    errors='replace',
                    env=env
                )
            
            # Lấy output
            if result.returncode == 0:
                output = result.stdout if result.stdout else "Code chạy thành công (không có output)"
                # Giới hạn độ dài output
                if len(output) > 5000:
                    output = output[:5000] + "\n...(output bị cắt do quá dài)"
                success = True
            else:
                error_output = result.stderr if result.stderr else "Lỗi không xác định"
                if len(error_output) > 2000:
                    error_output = error_output[:2000] + "\n...(lỗi bị cắt)"
                output = f"Lỗi thực thi:\n{error_output}"
                success = False
                
        except subprocess.TimeoutExpired:
            output = "Lỗi: Code chạy quá lâu (timeout 5 giây)"
            success = False
        except FileNotFoundError:
            output = f"Lỗi: Không tìm thấy {language} interpreter trên hệ thống"
            success = False
        except Exception as e:
            output = f"Lỗi hệ thống: {str(e)}"
            success = False
        finally:
            # Xóa file tạm
            try:
                os.unlink(temp_file_path)
            except:
                pass
        
        return JsonResponse({
            'output': output,
            'success': success,
            'language': language
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'output': 'Lỗi: Dữ liệu JSON không hợp lệ',
            'success': False
        })
    except Exception as e:
        return JsonResponse({
            'output': f'Lỗi server: {str(e)}',
            'success': False
        })

