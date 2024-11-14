from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path("IC_Main/", views.index, name='IC_Main'),
    path("IC_Main/selected/",views.index_with_userid_selected_date, name = 'IC_Main_selected'),
    path("IC_Main/download_excel/", views.download_excel, name='download_excel'),
    
]
