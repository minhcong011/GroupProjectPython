from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Tùy chỉnh giao diện admin cho User nếu cần
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

# Tùy chỉnh tiêu đề admin
admin.site.site_header = "Quản trị hệ thống"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Chào mừng đến với trang quản trị"
