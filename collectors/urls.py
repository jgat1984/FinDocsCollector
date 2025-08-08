from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# ✅ Custom JSON error handlers
def custom_404(request, exception):
    return JsonResponse({"error": "Not found"}, status=404)

def custom_500(request):
    return JsonResponse({"error": "Internal server error"}, status=500)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('collectors.urls')),
]

# ✅ Ensure all errors return JSON
handler404 = "backend.urls.custom_404"
handler500 = "backend.urls.custom_500"
