from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Account
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import random

def home(request):
    fname = request.user.first_name if request.user.is_authenticated else ""
    return render(request, "authentication/index.html", {"fname": fname})

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

        # Cho phép nhiều account dùng cùng email
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
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['pass1']
            )
            user.first_name = user_data['fname']
            user.last_name = user_data['lname']
            user.save()

            request.session.pop('otp')
            request.session.pop('temp_user')

            #Tạo user phân để check phân quyền
            username = user_data['username']
            is_teacher = user_data['is_teacher']
            
            Account.objects.create(username=username, is_teacher=is_teacher)
            messages.success(request, "Account created. Please sign in.")
            return redirect('signin')
        else:
            messages.error(request, "Invalid OTP.")
            return redirect('verify_otp')

    return render(request, "authentication/verify_otp.html")

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass1')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/cv/')  # Đăng nhập xong chuyển sang trang "Tôi"
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('signin')

    return render(request, "authentication/signin.html")

def signout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Logged out.")
    return redirect('home')
