# Đã xoá model Account khỏi app authentication để tránh trùng lặp với core.models.Account
# Nếu app này không còn model nào, bạn chỉ cần để file trống hoặc chỉ giữ import models nếu cần thiết cho migration

from django.db import models