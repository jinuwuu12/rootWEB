from django.contrib import admin
from django.urls import include, path

from mainApp import views

urlpatterns = [
    path('login_page/', views.login_page, name='login_page'),
    path('', views.login_button, name='login_button'),
    path('signup/', views.signup_button, name='signup_button'),
]