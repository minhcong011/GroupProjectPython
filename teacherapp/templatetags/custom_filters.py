import os
from django import template

register = template.Library()

@register.filter
def basename(value):
    """Lấy tên file từ đường dẫn"""
    if value:
        return os.path.basename(str(value))
    return value
