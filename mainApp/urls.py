from django.contrib import admin
from django.urls import include, path

from mainApp import views

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('login_page', views.login_page1, name='login_page1'),
    path('signup_page', views.signup_button, name = 'signup_button'),
    path('', views.getUserInfo, name='getUserInfo')
]