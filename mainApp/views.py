from django.shortcuts import render, redirect
import os
from rootWEB.views import index
# Create your views here.
def login_page(request):
    from django.conf import settings
    print(settings.BASE_DIR)  # BASE_DIR 확인
    print(os.path.join(settings.BASE_DIR, 'templates'))  # 템플릿 경로 확인
    
    return render(request, 'loginpage.html')

def login_button():
    return index()

def signup_button(request):
    return render(request, 'signup.html')
        