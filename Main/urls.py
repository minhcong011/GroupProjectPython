"""
URL configuration for Main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from core.admin_site import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),  # Sử dụng custom admin site
    path('django-admin/', admin.site.urls),  # Giữ lại admin mặc định cho backup
    path('', include('authentication.urls')),
    path('', include('cv.urls')), 
    path('', include('core.urls')),  # Core API endpoints
    path('', include('teacherapp.urls')),
    path('', include('AIapp.urls')),  # URL cho AIapp
    path('student/', include(('studentapp.urls', 'studentapp'), namespace='studentapp')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
