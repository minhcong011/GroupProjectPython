from django.shortcuts import render

def cv_edit(request):
    # Dữ liệu mẫu, sau này sẽ lấy từ database
    context = {
        'email': 'huyta152@gmail.com',
        'first_name': 'huy',
        'last_name': 'Tạ',
        'address': '',  # Đổi từ company sang address
        'title': '',
        'timezone': '',
        'phone_number': '0902327458',
    }
    return render(request, 'cv/cv.html', context)

def password_2fa(request):
    return render(request, 'cv/password_2fa.html')
