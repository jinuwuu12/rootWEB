from django.urls import path
from . import views

urlpatterns = [
    path("before_scan/", views.upload_page_view, name = 'before_scan'),
    path('scan_result/', views.barcode_reading_view, name='scan_result'),
    path('test/', views.test, name = 'test'),
    path('run/', views.scan_and_save_barcodes, name = 'run'),
    path('test_result/', views.render_product_info, name = 'test_result'),
    # path('debugging/', views.debugging, name='debugging')
]

