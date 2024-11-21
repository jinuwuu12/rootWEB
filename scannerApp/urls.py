from django.urls import path
from . import views

urlpatterns = [
    path("before_scan/", views.upload_page_view, name = 'before_scan'),
    path('scan_result/', views.barcode_reading_view, name='scan_result'),
    path('scan/', views.scan, name = 'scan'),
    path('run/', views.scan_and_save_barcodes, name = 'run'),
    path('result/', views.render_product_info, name = 'result'),
    path('update_product/', views.update_product, name='update_product'),
    # path('debugging/', views.debugging, name='debugging')
]
