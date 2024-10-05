from django.contrib import admin
from django.urls import path, include

from mainApp import views

urlpatterns = [
    path('login_page/', views.login_page, name='login_page'),
]