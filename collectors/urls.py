from django.urls import path
from .views import company_data_view, upload_to_drive

urlpatterns = [
    path('company/<str:ticker>/', company_data_view),
    path('upload/', upload_to_drive),
]
