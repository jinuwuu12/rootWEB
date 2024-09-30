from django.contrib import admin
from django.urls import path, include
from . import views  


urlpatterns = [
    path("IF_Main/", views.index, name='IF_Main'),
]