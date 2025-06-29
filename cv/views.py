from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Account

@login_required
def cv_edit(request):
    try:
        account = Account.objects.get(username=request.user.username)
        context = {
            'email': account.email or '',
            'first_name': account.first_name or '',
            'last_name': account.last_name or '',
            'address': account.company or '',  # Nếu muốn đổi sang address, hãy sửa model
            'title': account.title or '',
            'timezone': account.timezone or '',
            'phone_number': account.phone_number or '',
        }
    except Account.DoesNotExist:
        context = {}

    return render(request, 'cv/cv.html', context)

@login_required
def cvsv_edit(request):
    try:
        account = Account.objects.get(username=request.user.username)
        context = {
            'email': account.email or '',
            'first_name': account.first_name or '',
            'last_name': account.last_name or '',
            'address': account.company or '',  # Sử dụng đúng trường address cho sinh viên
            'title': account.title or '',
            'timezone': account.timezone or '',
            'phone_number': account.phone_number or '',
        }
    except Account.DoesNotExist:
        context = {}

    return render(request, 'cv/cvsv.html', context)

@login_required
def password_2fa(request):
    return render(request, 'cv/password_2fa.html')