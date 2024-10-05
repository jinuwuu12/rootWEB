
from django.contrib import admin
from django.urls import path, include
from . import views  # 메인 페이지 뷰 가져오기


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='main_page'),
    path('scanner/', include('scannerApp.urls')),  # scannerApp의 URL을 포함시킴
    path('main/', include('mainApp.urls')),     # mainApp의 URL을 포함시킴
    path('inventoryflow/',include('inventoryflowApp.urls')),
    path('inventorycheck/',include('inventorycheckApp.urls')),
]
