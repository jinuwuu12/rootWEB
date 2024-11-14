
from django.contrib import admin
from django.urls import path, include
from . import views  # 메인 페이지 뷰 가져오기


from django.conf import settings  # settings 임포트
from django.conf.urls.static import static  # static 함수 임포트


urlpatterns = [
    path('', views.index, name='main_page'),
    path('main/', include('mainApp.urls')),
    path('scanner/', include('scannerApp.urls')),  # scannerApp의 URL을 포함시킴
    path('inventoryflow/',include('inventoryflowApp.urls')),
    path('inventorycheck/',include('inventorycheckApp.urls')),
    path("admin/", admin.site.urls),
    
]


# 개발 환경에서 미디어 파일 제공 설정
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


