﻿from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('collectors.urls')),  # ✅ Routes all API calls to collectors
    re_path(r'^.*$', TemplateView.as_view(template_name="index.html")),  # React app entry
]
