from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from teacherapp.models import Course, BaiTap, CauHoi
from core.models import Lecture
from .models import DanhGiaKhoaHoc
from django.contrib.auth.models import User

import subprocess
import json
import tempfile
import os


def assignment_list(request):
    assignments = BaiTap.objects.all().order_by('-ngay_tao')
    return render(request, "student_page/assignment_list.html", {"assignments": assignments})

def ide_online(request):
    return render(request, "student_page/IDE_Onl.html")


def course(request):
    query = request.GET.get('q', '').strip()
    lang = request.GET.get('lang', '').strip()

    courses = Course.objects.all()

    # Lọc theo tên khóa học nếu chọn Python/Perl
    if lang in ['Python', 'Perl']:
        courses = courses.filter(name__icontains=lang)

    # Lọc tiếp theo từ khóa tìm kiếm
    if query:
        courses = courses.filter(name__icontains=query)

    context = {
        'courses': courses,
        'query': query,
        'filter_lang': lang,
    }
    return render(request, "student_page/course.html", context)


@csrf_exempt
@require_POST
def increment_participants(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            course_id = data.get("id")
            course = Course.objects.get(id=course_id)
            course.participants += 1
            course.save()
            return JsonResponse({"success": True, "participants": course.participants})
        except Course.DoesNotExist:
            return JsonResponse({"success": False, "error": "Course not found"})
    return JsonResponse({"success": False, "error": "Invalid method"})

def chatbot(request):
    return render(request, "student_page/Chat_bot.html")

def nop_bai(request, assignment_id=None):
    assignment = None
    if assignment_id:
        assignment = get_object_or_404(BaiTap, id=assignment_id)
    
    context = {'assignment': assignment}
    
    if request.method == "POST":
        if 'code' in request.POST:
            code = request.POST.get('code')
            language = request.POST.get('language')
            context['message'] = "Đã nhận code. (Chưa xử lý lưu/chấm thực tế)"
        elif 'file' in request.FILES:
            file = request.FILES['file']
            
            # Kiểm tra kích thước file (10MB)
            if file.size > 10 * 1024 * 1024:  # 10MB
                context['error'] = "File quá lớn! Vui lòng chọn file nhỏ hơn 10MB."
            else:
                # Kiểm tra định dạng file
                allowed_extensions = ['.py', '.pl', '.zip', '.rar', '.pdf', '.doc', '.docx', '.txt']
                file_name = file.name.lower()
                if not any(file_name.endswith(ext) for ext in allowed_extensions):
                    context['error'] = "Định dạng file không được hỗ trợ! Vui lòng chọn file: .py, .pl, .zip, .rar, .pdf, .doc, .docx, .txt"
                else:
                    # Lưu file vào database
                    if assignment and request.user.is_authenticated:
                        from teacherapp.models import BaiLam
                        bai_lam, created = BaiLam.objects.get_or_create(
                            sinh_vien=request.user,
                            bai_tap=assignment,
                            defaults={
                                'file_nop': file,
                                'da_cham': False
                            }
                        )
                        
                        if not created:
                            # Cập nhật file nếu đã tồn tại
                            bai_lam.file_nop = file
                            bai_lam.da_cham = False
                            bai_lam.save()
                    
                    context['submitted_file'] = {
                        'name': file.name,
                        'size': file.size,
                        'time': timezone.now()
                    }
                    context['message'] = f"Đã nộp file thành công: {file.name} ({file.size} bytes)"
    
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

def lecture_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lectures = Lecture.objects.filter(course=course).order_by('created_at')
    return render(request, "student_page/lecture_list.html", {"course": course, "lectures": lectures})


@login_required
def danh_gia_khoa_hoc(request):
    """View hiển thị trang đánh giá khóa học"""
    # Lấy các bài tập để sinh viên có thể đánh giá cụ thể
    bai_tap_list = BaiTap.objects.all().order_by('-ngay_tao')
    
    # Lấy danh sách khóa học
    khoa_hoc_list = Course.objects.all().order_by('name')
    
    # Lấy danh sách giảng viên (users có quyền staff hoặc superuser)
    giang_vien_list = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).order_by('first_name', 'last_name')
    
    # Lấy đánh giá đã gửi của sinh viên hiện tại
    danh_gia_da_gui = DanhGiaKhoaHoc.objects.filter(sinh_vien=request.user).order_by('-ngay_tao')
    
    context = {
        'title': 'Đánh giá khóa học',
        'bai_tap_list': bai_tap_list,
        'khoa_hoc_list': khoa_hoc_list,
        'giang_vien_list': giang_vien_list,
        'danh_gia_da_gui': danh_gia_da_gui,
    }
    return render(request, 'student_page/danh_gia_khoa_hoc.html', context)


@login_required
def gui_danh_gia(request):
    """View xử lý gửi đánh giá từ sinh viên"""
    if request.method == 'POST':
        loai_danh_gia = request.POST.get('loai_danh_gia')
        khoa_hoc_id = request.POST.get('khoa_hoc_id')
        bai_tap_id = request.POST.get('bai_tap_id')
        giang_vien_id = request.POST.get('giang_vien_id')
        diem_sao = request.POST.get('diem_sao')
        tieu_de = request.POST.get('tieu_de')
        noi_dung = request.POST.get('noi_dung')
        gop_y = request.POST.get('gop_y')
        
        # Validation
        if not all([loai_danh_gia, diem_sao, tieu_de, noi_dung]):
            messages.error(request, 'Vui lòng điền đầy đủ thông tin bắt buộc!')
            return redirect('studentapp:danh_gia_khoa_hoc')
        
        try:
            # Tạo đánh giá mới
            danh_gia = DanhGiaKhoaHoc(
                sinh_vien=request.user,
                loai_danh_gia=loai_danh_gia,
                diem_sao=int(diem_sao),
                tieu_de=tieu_de,
                noi_dung=noi_dung,
                gop_y=gop_y or None
            )
            
            # Gán đối tượng đánh giá tương ứng
            if loai_danh_gia == 'khoa_hoc' and khoa_hoc_id:
                khoa_hoc = get_object_or_404(Course, id=khoa_hoc_id)
                danh_gia.khoa_hoc = khoa_hoc
            elif loai_danh_gia == 'bai_tap' and bai_tap_id:
                bai_tap = get_object_or_404(BaiTap, id=bai_tap_id)
                danh_gia.bai_tap = bai_tap
            elif loai_danh_gia == 'giang_vien' and giang_vien_id:
                giang_vien = get_object_or_404(User, id=giang_vien_id)
                danh_gia.giang_vien = giang_vien
            else:
                messages.error(request, 'Vui lòng chọn đối tượng đánh giá phù hợp!')
                return redirect('studentapp:danh_gia_khoa_hoc')
            
            danh_gia.save()
            messages.success(request, 'Đánh giá đã được gửi thành công! Cảm ơn bạn đã góp ý.')
            
        except Exception as e:
            messages.error(request, f'Có lỗi xảy ra: {str(e)}')
        
        return redirect('studentapp:danh_gia_khoa_hoc')
    
    return redirect('studentapp:danh_gia_khoa_hoc')

