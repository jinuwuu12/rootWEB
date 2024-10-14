from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path("IC_Main/", views.index, name='IC_Main'),
    path("IC_Main/userID/",views.index_with_userid, name = 'IC_Main_userID'),
    path("IC_Main/download_excel/", views.download_excel, name='download_excel'),
    
]
