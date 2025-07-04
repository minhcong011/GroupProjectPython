from django.shortcuts import render, redirect
from django.utils import timezone
from teacherapp.models import Course  # Thêm import model Course

def assignment_list(request):
    
    return render(request, "student_page/assignment_list.html")

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
