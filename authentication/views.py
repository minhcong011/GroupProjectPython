from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from core.models import Account
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def home(request):
    return render(request, "authentication/index.html")

def send_otp_to_email(email, otp):
    subject = 'Mã xác thực đăng nhập - PERL & PYTHON'
    message = f'Mã xác thực đăng nhập của bạn là: {otp}\n\nMã này có hiệu lực trong 5 phút.'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

def signup(request):
    if request.method == "POST":
        account_type = request.POST.get('account_type')
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        is_teacher = (account_type == 'teacher')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        # Tạo tài khoản trực tiếp không cần OTP
        user = User.objects.create_user(
            username=username,
            email=email,
            password=pass1
        )
        user.first_name = fname
        user.last_name = lname
        user.save()

        Account.objects.create(
            username=user.username,
            is_teacher=is_teacher,
            email=user.email,
            is_email_verified=True,
            first_name=user.first_name,
            last_name=user.last_name
        )

        messages.success(request, "Tài khoản đã được tạo thành công! Vui lòng đăng nhập.")
        return redirect('signin')

    return render(request, "authentication/signup.html")

def signin(request):
    if request.user.is_authenticated:
        try:
            account = Account.objects.get(username=request.user.username)
            if account.is_teacher:
                return redirect('teacher_home')
            else:
                return redirect('student_home')
        except Account.DoesNotExist:
            logout(request)
            return redirect('signin')

    if request.method == "POST":
        # Kiểm tra nếu đang xác thực OTP
        if 'verify_otp' in request.POST:
            entered_otp = request.POST.get('otp')
            session_otp = request.session.get('login_otp')
            temp_login = request.session.get('temp_login')

            if entered_otp == session_otp and temp_login:
                user = User.objects.get(username=temp_login['username'])
                account = Account.objects.get(username=user.username)
                
                login(request, user)
                
                # Xử lý remember me
                if temp_login.get('remember_me'):
                    request.session.set_expiry(60 * 60 * 24 * 30)  
                else:
                    request.session.set_expiry(0)
                
                # Xóa session tạm
                request.session.pop('login_otp')
                request.session.pop('temp_login')
                
                # Chuyển hướng theo vai trò
                if account.is_teacher:
                    return redirect('teacher_home')
                else:
                    return redirect('student_home')
            else:
                messages.error(request, "Mã OTP không đúng.")
                return render(request, "authentication/signin_otp.html")
        
        # Đăng nhập bước 1: kiểm tra username/password
        else:
            username = request.POST.get('username')
            password = request.POST.get('pass1')
            remember_me = request.POST.get('remember_me')

            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    account = Account.objects.get(username=user.username)
                except Account.DoesNotExist:
                    messages.error(request, "Account data error. Please contact admin.")
                    return redirect('signin')

                # Kiểm tra nếu user đã bật 2FA
                if account.two_factor_enabled:
                    # Tạo OTP và gửi email
                    otp = str(random.randint(100000, 999999))
                    send_otp_to_email(user.email, otp)
                    
                    # Lưu thông tin tạm vào session
                    request.session['login_otp'] = otp
                    request.session['temp_login'] = {
                        'username': username,
                        'remember_me': remember_me == "on"
                    }
                    
                    messages.success(request, f"Mã OTP đã được gửi đến email {user.email}")
                    return render(request, "authentication/signin_otp.html")
                else:
                    # Đăng nhập trực tiếp nếu chưa bật 2FA
                    login(request, user)
                    
                    # Xử lý remember me
                    if remember_me == "on":
                        request.session.set_expiry(60 * 60 * 24 * 30)  
                    else:
                        request.session.set_expiry(0)
                    
                    # Chuyển hướng theo vai trò
                    if account.is_teacher:
                        return redirect('teacher_home')
                    else:
                        return redirect('student_home')
            else:
                messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
                return redirect('signin')

    return render(request, "authentication/signin.html")

    
def teacher_home(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    try:
        account = Account.objects.get(username=request.user.username)
        if not account.is_teacher:
            return redirect('student_home')
    except Account.DoesNotExist:
        return redirect('signin')
    return render(request, "authentication/indexgv.html")

def student_home(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    try:
        account = Account.objects.get(username=request.user.username)
        if account.is_teacher:
            return redirect('teacher_home')
    except Account.DoesNotExist:
        return redirect('signin')
    return render(request, "authentication/indexsv.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out.")
    return redirect('home')