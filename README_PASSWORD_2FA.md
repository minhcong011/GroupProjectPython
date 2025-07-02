# Password & 2FA Feature Documentation

## Tổng quan
Trang **Bảo mật & Xác thực** (`password_2fa.html`) đã được triển khai với đầy đủ chức năng:

### 1. Đổi mật khẩu
- **URL**: `/cv/password_2fa/`
- **Chức năng**: Cho phép người dùng thay đổi mật khẩu hiện tại
- **Xác thực**: 
  - Kiểm tra mật khẩu hiện tại
  - Xác nhận mật khẩu mới phải khớp
  - Mật khẩu mới tối thiểu 8 ký tự
  - Tự động cập nhật session để không bị logout

### 2. Xác thực 2 yếu tố (2FA)
- **Chức năng**: Bật/tắt xác thực 2 yếu tố
- **Lưu trữ**: Trạng thái được lưu trong database (`Account.two_factor_enabled`)
- **Logic đăng nhập**:
  - Nếu 2FA **TẮT**: Đăng nhập trực tiếp sau khi nhập username/password
  - Nếu 2FA **BẬT**: Yêu cầu nhập mã OTP gửi qua email

## Files đã được cập nhật:

### 1. Models (`core/models.py`)
```python
class Account(models.Model):
    # ... existing fields ...
    two_factor_enabled = models.BooleanField(default=False)  # NEW FIELD
```

### 2. Views (`cv/views.py`)
- **`password_2fa(request)`**: Xử lý cả đổi mật khẩu và toggle 2FA
- **Form actions**:
  - `action=change_password`: Đổi mật khẩu
  - `action=toggle_2fa`: Bật/tắt 2FA

### 3. Authentication (`authentication/views.py`)
- **`signin(request)`**: Cập nhật logic kiểm tra 2FA
- **Logic**:
  - Kiểm tra `account.two_factor_enabled`
  - Nếu `True`: Gửi OTP qua email
  - Nếu `False`: Đăng nhập trực tiếp

### 4. Template (`templates/cv/password_2fa.html`)
- **Form đổi mật khẩu**: 3 trường (mật khẩu hiện tại, mới, xác nhận)
- **Toggle 2FA**: Switch button hiển thị trạng thái hiện tại
- **Responsive design**: Tương thích mobile
- **Messages**: Hiển thị thông báo thành công/lỗi

### 5. Styles (`static/css/password_2fa.css`)
- **Form styling**: Modern, clean design
- **Toggle switch**: Animated switch với màu sắc trạng thái
- **Status indicators**: 
  - Xanh lá = 2FA enabled
  - Đỏ = 2FA disabled
- **Responsive**: Mobile-friendly

## Migration
```bash
python manage.py makemigrations core
python manage.py migrate
```

## Cách sử dụng:

### Đổi mật khẩu:
1. Nhập mật khẩu hiện tại
2. Nhập mật khẩu mới (tối thiểu 8 ký tự)
3. Xác nhận mật khẩu mới
4. Click "Đổi mật khẩu"

### Bật/Tắt 2FA:
1. Click toggle switch
2. Click "Lưu cài đặt bảo mật"
3. Hệ thống sẽ cập nhật trạng thái trong database

## Lợi ích của 2FA:
- 🔒 **Bảo vệ khỏi truy cập trái phép**: Ngay cả khi mật khẩu bị lộ
- 📱 **Xác thực qua email**: Mã OTP gửi đến email đã đăng ký
- 🚫 **Ngăn chặn đăng nhập lạ**: Chỉ thiết bị có email mới đăng nhập được
- ⚡ **Dễ sử dụng**: Chỉ cần kiểm tra email và nhập mã 6 số

## Testing:
1. Đăng nhập vào hệ thống
2. Truy cập `/cv/password_2fa/`
3. Test đổi mật khẩu với các trường hợp:
   - Mật khẩu hiện tại sai
   - Mật khẩu mới không khớp
   - Mật khẩu mới quá ngắn
   - Đổi thành công
4. Test bật/tắt 2FA:
   - Bật 2FA → Logout → Login (cần OTP)
   - Tắt 2FA → Logout → Login (không cần OTP)
