# Education Management System

Hệ thống quản lý giáo dục được xây dựng bằng Django, hỗ trợ đầy đủ tính năng cho giáo viên và sinh viên.

## Mục lục

- [Tính năng chính](#tính-năng-chính)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Cài đặt](#cài-đặt)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Sử dụng](#sử-dụng)
- [License](#license)

## Tính năng chính

### Dành cho Sinh viên
- Quản lý khóa học: Xem danh sách khóa học, tài liệu học tập
- Bài tập: Nộp bài tập, xem điểm số và nhận xét
- Thống kê học tập: Dashboard cá nhân với biểu đồ tiến độ
- Đánh giá: Đánh giá khóa học, bài tập và giảng viên
- Thông báo hệ thống: Nhận thông báo về bài tập, điểm số, sự kiện
- CV Generator: Tạo CV chuyên nghiệp tự động

### Dành cho Giáo viên
- Quản lý khóa học: Tạo, chỉnh sửa khóa học và tài liệu
- Tạo bài tập: Đưa ra bài tập với deadline và hướng dẫn
- Chấm điểm: Chấm bài và đưa ra nhận xét chi tiết
- AI Assistant: Tạo câu hỏi tự động, gợi ý nội dung
- Báo cáo: Thống kê học tập của sinh viên
- Quản lý lớp học: Theo dõi tiến độ học tập

### Quản trị hệ thống
- Quản lý người dùng: Admin panel với đầy đủ tính năng
- Hệ thống email: Gửi thông báo tự động
- Bảo mật: Xác thực đa lớp, phân quyền chi tiết
- Responsive: Tương thích mọi thiết bị

## Công nghệ sử dụng

### Backend
- Django 5.2.3 - Web framework chính
- Python 3.13+ - Ngôn ngữ lập trình
- SQLite - Cơ sở dữ liệu

### Frontend
- HTML5 & CSS3 - Giao diện cơ bản
- Bootstrap 5 - CSS framework
- JavaScript - Tương tác động
- Chart.js - Biểu đồ thống kê

## Cài đặt

### Yêu cầu hệ thống
- Python 3.13+
- pip
- Git

### 1. Clone repository
```bash
git clone https://github.com/minhcong011/GroupProjectPython.git
cd GroupProjectPython
```

### 2. Tạo môi trường ảo
```bash
# Windows
python -m venv env
env\\Scripts\\activate

# macOS/Linux
python3 -m venv env
source env/bin/activate
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Tạo superuser
```bash
python manage.py createsuperuser
```

### 6. Chạy server
```bash
python manage.py runserver
```

Truy cập: http://127.0.0.1:8000

## Cấu trúc dự án

```
GroupProjectPython/
├── Main/                      # Cấu hình Django chính
│   ├── settings.py           # Cài đặt dự án
│   ├── urls.py              # URL routing chính
│   └── wsgi.py              # WSGI configuration
├── authentication/          # App xác thực người dùng
│   ├── models.py            # User models
│   ├── views.py             # Login/Register views
│   └── forms.py             # Authentication forms
├── core/                    # App core
│   ├── models.py            # Shared models
│   ├── middleware.py        # Custom middleware
│   └── utils.py             # Utility functions
├── teacherapp/              # App dành cho giáo viên
│   ├── models.py            # Course, Assignment models
│   ├── views.py             # Teacher dashboard, grading
│   ├── forms.py             # Course creation forms
│   └── random_question_ai.py # AI question generation
├── studentapp/              # App dành cho sinh viên
│   ├── models.py            # Student progress, notifications
│   ├── views.py             # Student dashboard, submissions
│   └── admin.py             # Admin interface
├── AIapp/                   # App tích hợp AI
│   ├── models.py            # AI interaction models
│   ├── views.py             # AI-powered features
│   └── utils.py             # AI utility functions
├── cv/                      # App tạo CV
│   ├── models.py            # CV templates
│   └── views.py             # CV generation
├── templates/               # HTML templates
│   ├── authentication/     # Login/Register templates
│   ├── teacher_page/        # Teacher interface
│   ├── student_page/        # Student interface
│   └── admin/               # Admin templates
├── static/                  # Static files
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript files
│   └── image/               # Images and icons
├── uploads/                 # File uploads
├── db.sqlite3               # Database file
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md                # Documentation
```

## Sử dụng

### Đăng nhập hệ thống

1. Admin: http://127.0.0.1:8000/admin/
   - Quản lý toàn bộ hệ thống
   - Tạo người dùng mới
   - Cấu hình hệ thống

2. Giáo viên: http://127.0.0.1:8000/teacher/
   - Dashboard quản lý khóa học
   - Tạo và chấm bài tập
   - Xem thống kê sinh viên

3. Sinh viên: http://127.0.0.1:8000/student/
   - Xem khóa học và bài tập
   - Nộp bài và xem điểm
   - Nhận thông báo

### Quy trình sử dụng cơ bản

#### Dành cho Giáo viên:
1. Tạo khóa học mới
   - Vào Teacher Dashboard
   - Click "Tạo khóa học"
   - Điền thông tin và upload tài liệu

2. Tạo bài tập
   - Chọn khóa học
   - Click "Tạo bài tập"
   - Sử dụng AI để tạo câu hỏi

3. Chấm điểm
   - Vào "Quản lý bài nộp"
   - Xem bài làm của sinh viên
   - Đưa ra điểm và nhận xét

#### Dành cho Sinh viên:
1. Tham gia khóa học
   - Đăng nhập vào Student Dashboard
   - Xem danh sách khóa học
   - Click vào khóa học để học

2. Làm bài tập
   - Vào mục "Bài tập"
   - Chọn bài tập cần làm
   - Upload file hoặc nhập text

3. Xem kết quả
   - Kiểm tra điểm số
   - Đọc nhận xét từ giáo viên
   - Xem thống kê tiến độ

## License

Dự án này được phát hành dưới MIT License. Xem file LICENSE để biết thêm chi tiết.

## Liên hệ

- Email: phuockhoamai@gmail.com
- GitHub: https://github.com/minhcong011/GroupProjectPython
- Issues: https://github.com/minhcong011/GroupProjectPython/issues
