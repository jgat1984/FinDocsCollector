from django.urls import path, re_path
from . import views

urlpatterns = [
    # Accepts /api/company/MSFT or /api/company/MSFT/
    re_path(r'^company/(?P<ticker>[\w\.-]+)/?$', views.company_data_view, name='company_data'),
    # Accepts POST to /api/upload/
    path('upload/', views.upload_to_drive, name='upload_to_drive'),
]
