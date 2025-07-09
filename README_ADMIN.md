# Admin Dashboard cho Hệ thống EduSync

## 🎯 Tổng quan
Admin Dashboard được thiết kế theo mô hình hiện đại với giao diện dễ sử dụng, bao gồm đầy đủ các chức năng quản trị cho hệ thống học tập.

## 🚀 Các tính năng chính

### 1. Dashboard Tổng quan
- **URL**: `/admin-dashboard/`
- Hiển thị thống kê tổng số: học viên, khóa học, bài tập, bài giảng
- Người dùng mới trong tuần
- Hoạt động gần đây
- Biểu đồ thống kê

### 2. Quản lý Khóa học
- **URL**: `/admin-dashboard/courses/`
- Danh sách khóa học với phân trang
- Thêm/Sửa/Xóa khóa học
- Tìm kiếm và lọc
- Gán giảng viên cho khóa

### 3. Quản lý Bài tập
- **URL**: `/admin-dashboard/assignments/`
- Quản lý bài tập Python/Perl
- Đặt deadline, miêu tả
- Xem thống kê số lượt nộp

### 4. Quản lý Người dùng
- **URL**: `/admin-dashboard/users/`
- Danh sách tất cả người dùng
- Tìm kiếm theo vai trò
- Phân quyền (is_staff, is_superuser)
- Gán vai trò giảng viên/học viên

### 5. Quản lý Bài giảng
- **URL**: `/admin-dashboard/lectures/`
- Upload video, PDF, slide
- Phân loại theo môn học
- Quản lý tài liệu đính kèm

### 6. Thống kê & Báo cáo
- **URL**: `/admin-dashboard/statistics/`
- Biểu đồ hoạt động theo thời gian
- Phân bố người dùng
- Top khóa học phổ biến
- Xuất báo cáo PDF/Excel/CSV

## 🛠️ Cài đặt và Chạy

### 1. Cấu hình Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Tạo Superuser
```bash
python manage.py createsuperuser
```

### 3. Chạy Server
```bash
python manage.py runserver 8888
```

### 4. Truy cập Admin Dashboard
- **Django Admin mặc định**: http://localhost:8888/admin/
- **Admin Dashboard tùy chỉnh**: http://localhost:8888/admin-dashboard/

## 📂 Cấu trúc Files

```
admin_panel/
├── views.py              # Các view cho admin dashboard
├── urls.py               # URL routing
├── admin.py              # Cấu hình Django admin
├── models.py             # Models (sử dụng models từ app khác)
└── templates/admin_panel/
    ├── dashboard.html        # Trang dashboard chính
    ├── course_list.html      # Danh sách khóa học
    ├── course_form.html      # Form thêm/sửa khóa học
    ├── assignment_list.html  # Danh sách bài tập
    ├── user_list.html        # Danh sách người dùng
    ├── lecture_list.html     # Danh sách bài giảng
    └── statistics.html       # Trang thống kê
```

## 🔐 Phân quyền

### AdminRequiredMixin
Tất cả view đều sử dụng `AdminRequiredMixin` để kiểm tra quyền:
- Phải đăng nhập (`LoginRequiredMixin`)
- Phải có quyền staff hoặc superuser (`UserPassesTestMixin`)

### Các vai trò:
- **Superuser**: Toàn quyền truy cập
- **Staff**: Có thể truy cập admin dashboard
- **Teacher**: Có thể tạo bài tập và bài giảng
- **Student**: Chỉ có thể xem và làm bài

## 🎨 Giao diện

### Thiết kế:
- **Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Charts**: Chart.js
- **Color Scheme**: Blue gradient theme
- **Responsive**: Tối ưu cho desktop và mobile

### Sidebar Navigation:
- Dashboard
- Khóa học
- Bài tập  
- Bài giảng
- Người dùng
- Thông báo
- Chatbot
- Thống kê
- Cài đặt
- Đăng xuất

## 📊 Biểu đồ và Thống kê

### Dashboard chính:
- Cards thống kê tổng quan
- Biểu đồ line chart hoạt động
- Danh sách hoạt động gần đây
- Calendar widget

### Trang thống kê:
- Biểu đồ timeline theo ngày/tháng/năm
- Biểu đồ doughnut phân bố người dùng
- Bảng top khóa học phổ biến
- Metrics hiệu suất hệ thống

## 🔧 Tùy chỉnh

### Thêm chức năng mới:
1. Tạo view trong `views.py`
2. Thêm URL trong `urls.py`  
3. Tạo template trong `templates/admin_panel/`
4. Thêm link vào sidebar trong `dashboard.html`

### Thay đổi giao diện:
- Sửa CSS trong `<style>` tag của template
- Thêm JavaScript cho tương tác
- Sử dụng Bootstrap classes có sẵn

## 📝 Lưu ý quan trọng

1. **Security**: Tất cả view đều có kiểm tra quyền
2. **Pagination**: Danh sách có phân trang tự động
3. **Search**: Hỗ trợ tìm kiếm và lọc dữ liệu
4. **Responsive**: Giao diện thân thiện với mobile
5. **Performance**: Sử dụng select_related và prefetch_related khi cần

## 🆘 Troubleshooting

### Lỗi thường gặp:

1. **TemplateDoesNotExist**: Kiểm tra đường dẫn template
2. **NoReverseMatch**: Kiểm tra tên URL trong urls.py
3. **PermissionDenied**: User chưa có quyền is_staff
4. **Static files không load**: Chạy `collectstatic` cho production

### Debug mode:
- Bật `DEBUG = True` trong settings.py
- Kiểm tra console browser cho lỗi JavaScript
- Xem Django debug toolbar

## 🎁 Tính năng bonus

- Dark/Light mode toggle
- Export dữ liệu PDF/Excel
- Notification real-time
- Advanced search filters
- Bulk actions
- Activity logging
