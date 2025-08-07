from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.urls import path, include, re_path
from collectors.views import company_data_view


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/', include('collectors.urls')),  # ✅ Routes all API calls to collectors
    path('api/company/<str:ticker>', company_data_view),  # ✅ API first
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),  # ✅ React fallback LAST
]
