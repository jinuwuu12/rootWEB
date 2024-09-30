from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path("IC_Main/", views.index, name='IC_Main'),
]
