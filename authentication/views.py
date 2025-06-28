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
    subject = 'Xác thực tài khoản Django'
    message = f'Mã xác thực của bạn là: {otp}'
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

        otp = str(random.randint(100000, 999999))
        send_otp_to_email(email, otp)

        request.session['otp'] = otp
        request.session['temp_user'] = {
            'username': username,
            'fname': fname,
            'lname': lname,
            'email': email,
            'pass1': pass1,
            'is_teacher': is_teacher,
        }

        return redirect('verify_otp')

    return render(request, "authentication/signup.html")

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        user_data = request.session.get('temp_user')

        if entered_otp == session_otp and user_data:
            if User.objects.filter(username=user_data['username']).exists():
                messages.error(request, "Username already exists.")
                return redirect('signup')

            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['pass1']
            )
            user.first_name = user_data['fname']
            user.last_name = user_data['lname']
            user.save()

            is_teacher = user_data.get('is_teacher', False)
            Account.objects.create(
                username=user.username,
                is_teacher=is_teacher,
                email=user.email,
                is_email_verified=True,
                first_name=user.first_name,
                last_name=user.last_name
            )

            request.session.pop('otp')
            request.session.pop('temp_user')
            # KHÔNG tự động đăng nhập
            messages.success(request, "Email verified successfully. Please sign in.")
            return redirect('home')
        else:
            messages.error(request, "Invalid OTP.")
            return redirect('verify_otp')

    return render(request, "authentication/verify_otp.html")

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
        username = request.POST.get('username')
        password = request.POST.get('pass1')
        remember_me = request.POST.get('remember_me')  # Lấy giá trị checkbox
        print("remember_me:", remember_me)  # Debug: kiểm tra giá trị checkbox

        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                account = Account.objects.get(username=user.username)
                if not account.is_email_verified:
                    messages.error(request, "Please verify your email before signing in.")
                    return redirect('signin')
            except Account.DoesNotExist:
                messages.error(request, "Account data error. Please contact admin.")
                return redirect('signin')

            login(request, user)
            # Xử lý ghi nhớ đăng nhập
            if remember_me == "on":
                request.session.set_expiry(60 * 60 * 24 * 30)  # 30 ngày
            else:
                request.session.set_expiry(0)  # Hết hạn khi đóng trình duyệt

            if account.is_teacher:
                return redirect('teacher_home')
            else:
                return redirect('student_home')
        else:
            messages.error(request, "Invalid credentials.")
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