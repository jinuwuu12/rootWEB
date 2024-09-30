# views.py (예: 메인 앱이나 프로젝트의 views.py에 작성)
from django.shortcuts import render
import os

def index(request):
    from django.conf import settings
    print(settings.BASE_DIR)  # BASE_DIR 확인
    print(os.path.join(settings.BASE_DIR, 'templates'))  # 템플릿 경로 확인
    
    return render(request, 'mainpage.html')
