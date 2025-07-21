from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from core.models import Account
from django.utils import timezone

@login_required
def cv_edit(request):
    try:
        account = Account.objects.get(username=request.user.username)
    except Account.DoesNotExist:
        account = None

    if request.method == 'POST' and account:
        account.email = request.POST.get('email', '')
        account.first_name = request.POST.get('first_name', '')
        account.last_name = request.POST.get('last_name', '')
        account.phone_number = request.POST.get('phone_number', '')
        account.company = request.POST.get('address', '')
        account.save()
        return redirect('cv_edit')

    context = {
        'email': account.email if account else '',
        'first_name': account.first_name if account else '',
        'last_name': account.last_name if account else '',
        'address': account.company if account else '',
        'title': account.title if account else '',
        'timezone': account.timezone if account else '',
        'phone_number': account.phone_number if account else '',
    }
    
    if hasattr(account, 'is_teacher') and account.is_teacher:
        return render(request, 'cv/cv_teacher.html', context)
    else:
        return render(request, 'cv/cv_student.html', context)


@login_required
def password_2fa(request):
    """Trang đổi mật khẩu và cấu hình xác thực 2 yếu tố"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'change_password':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            
            if not request.user.check_password(current_password):
                messages.error(request, 'Mật khẩu hiện tại không đúng!')
                return redirect('cv:password_2fa')
            
            
            if new_password != confirm_password:
                messages.error(request, 'Mật khẩu xác nhận không khớp!')
                return redirect('cv:password_2fa')
            
            if len(new_password) < 8:
                messages.error(request, 'Mật khẩu mới phải có ít nhất 8 ký tự!')
                return redirect('cv:password_2fa')
            
            
            request.user.set_password(new_password)
            request.user.save()
            
            
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            
            messages.success(request, 'Mật khẩu đã được thay đổi thành công!')
            return redirect('cv:password_2fa')
            
        elif action == 'toggle_2fa':
            enable_2fa = request.POST.get('enable_2fa') == 'true'
            
            
            try:
                account = Account.objects.get(username=request.user.username)
                account.two_factor_enabled = enable_2fa
                account.save()
                
                if enable_2fa:
                    messages.success(request, 'Xác thực 2 yếu tố đã được bật! Bạn sẽ cần nhập mã OTP khi đăng nhập.')
                else:
                    messages.success(request, 'Xác thực 2 yếu tố đã được tắt.')
            except Account.DoesNotExist:
                messages.error(request, 'Không tìm thấy thông tin tài khoản!')
            
            return redirect('cv:password_2fa')
    
    return render(request, 'cv/password_2fa.html')

@login_required
def profile(request):
    try:
        account = Account.objects.get(username=request.user.username)
    except Account.DoesNotExist:
        account = None

    if request.method == 'POST' and account:
        
        if 'avatar' in request.FILES:
            account.avatar = request.FILES['avatar']
        
        
        account.email = request.POST.get('email', '')
        account.first_name = request.POST.get('first_name', '')
        account.last_name = request.POST.get('last_name', '')
        account.phone_number = request.POST.get('phone_number', '')
        account.company = request.POST.get('company', '')
        account.title = request.POST.get('title', '')
        account.timezone = request.POST.get('timezone', 'Asia/Ho_Chi_Minh')
        

        user = request.user
        user.email = account.email
        user.first_name = account.first_name
        user.last_name = account.last_name
        user.save()
        
        account.save()
        messages.success(request, 'Thông tin cá nhân đã được cập nhật thành công!')
        return redirect('cv:profile')

    context = {
        'account': account,
        'now': timezone.now(),
    }
    return render(request, 'cv/profile.html', context)