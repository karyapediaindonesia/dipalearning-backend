"""
URL configuration for dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.dashboard.urls', namespace='dashboard')),
    path('api/v1/', include('apps.accounts.urls')),
    path('api/v1/branches/', include('apps.branches.urls')),
    path('api/v1/academics/', include('apps.academics.urls')),
    path('api/v1/core/', include('apps.core.urls')),

    path('api/v1/audit-logs/', include('apps.audit.urls')),
    path('api/v1/attendance/', include('apps.attendance.urls')),
    path('api/v1/finance/', include('apps.finance.urls')),
    path('api/v1/students/', include('apps.students.urls')),
    path('api/v1/hr/', include('apps.hr.urls')),
    path('api/v1/billing/', include('apps.billing.urls')),
    path('api/v1/quotas/', include('apps.quotas.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import re_path
from apps.dashboard.views import page_error_404
urlpatterns += [
    re_path(r'^.*$', page_error_404),
]
