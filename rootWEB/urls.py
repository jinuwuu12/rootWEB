
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('scannerApp.urls')),  # scannerApp의 URL을 포함시킴
    path('scan_result/', include('scannerApp.urls')),
]
