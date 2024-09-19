from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_page_view),
    path('upload-barcode/', views.barcode_reading_view, name='upload_barcode'),
]

