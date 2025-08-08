from django.urls import path
from . import views

print("[DEBUG] collectors/urls.py loaded — API routes registered")

urlpatterns = [
    path('company/<str:ticker>/', views.company_data_view, name='company_data'),
    path('upload/', views.upload_to_drive, name='upload_to_drive'),  # ✅ Google Drive Upload API
]

print("[DEBUG] collectors/urls.py — urlpatterns set:")
for pattern in urlpatterns:
    print(f"    [DEBUG] Route registered: {pattern}")
