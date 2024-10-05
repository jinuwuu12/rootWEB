from django.shortcuts import render
import os
# Create your views here.
def login_page(request):
    from django.conf import settings
    print(settings.BASE_DIR)  # BASE_DIR 확인
    print(os.path.join(settings.BASE_DIR, 'templates'))  # 템플릿 경로 확인
    
    return render(request, 'loginpage.html')