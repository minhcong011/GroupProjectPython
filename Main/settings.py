from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-d9m)q&ykfk+r61vz3fs9=d14%bqn_89#f$at(_q$ibs6a%50ts'

DEBUG = True

ALLOWED_HOSTS = []

# ==================== ỨNG DỤNG ====================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'authentication',  # App xác thực
    'cv',  # App CV
    'core',  # App core
    'teacherapp',  # App giáo viên
    'studentapp',  # App sinh viên
    'AIapp'  # App AI
]

# ==================== MIDDLEWARE ====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.AdminLogMiddleware',  # Thêm middleware logging
]

ROOT_URLCONF = 'Main.urls'

# ==================== TEMPLATES ====================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Chỉ đến thư mục templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Main.wsgi.application'

# ==================== DATABASE ====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==================== PASSWORD VALIDATION ====================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==================== QUỐC TẾ HÓA & ENCODING ====================
LANGUAGE_CODE = 'vi-vn'  # Chuyển sang tiếng Việt
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

# Cấu hình encoding cho tiếng Việt
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'

# Cấu hình locale cho tiếng Việt
import locale
import os
os.environ.setdefault('LANG', 'vi_VN.UTF-8')
os.environ.setdefault('LC_ALL', 'vi_VN.UTF-8')

try:
    locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Vietnamese_Vietnam.1258')
    except:
        pass

# ==================== STATIC FILES ====================
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==================== CẤU HÌNH EMAIL (SMTP Gmail) ====================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'phuockhoamai@gmail.com'
EMAIL_HOST_PASSWORD = 'ajxzihidyzkcfrsa'        

# ==================== GROQ AI API CONFIGURATION ====================



# ==================== MEDIA FILES ====================
MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')