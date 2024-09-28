from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_page_view),
    path('scan_result/', views.barcode_reading_view, name='scan_result'),
    path('debugging/', views.debugging, name='debugging')
]

