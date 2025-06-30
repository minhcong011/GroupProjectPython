from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Account

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
        account.company = request.POST.get('address', '')  # đổi thành address nếu bạn rename trường trong model
        account.save()
        return redirect('cv_edit')  # hoặc redirect lại chính URL để load lại

    context = {
        'email': account.email if account else '',
        'first_name': account.first_name if account else '',
        'last_name': account.last_name if account else '',
        'address': account.company if account else '',
        'title': account.title if account else '',
        'timezone': account.timezone if account else '',
        'phone_number': account.phone_number if account else '',
    }
    return render(request, 'cv/cv.html', context)

@login_required
def password_2fa(request):
    return render(request, 'cv/password_2fa.html')