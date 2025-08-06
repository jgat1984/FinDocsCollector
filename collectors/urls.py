from django.urls import path
from . import views

urlpatterns = [
    path('company/<str:ticker>/', views.company_data_view, name='company_data'),
    path('upload/', views.upload_to_drive, name='upload_to_drive'),  # ✅ Google Drive Upload API
]
