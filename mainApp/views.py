from django.shortcuts import render, redirect
import os
from rootWEB.views import index
from .models import user_info
from django.contrib import messages  # 메시지를 추가로 사용할 수 있습니다.
# Create your views here.
# 메인이랑 연결시켜주는거
def login_page1(request):
    return render(request, 'loginpage.html')
# 메인이랑 연결시켜주는거
def signup_button(request):
    return render(request, 'signup.html')

#ㄹㅇ 로그인버튼
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('user_id')
        password = request.POST.get('user_password')
        print(username, password)
        try:
            # 데이터베이스에서 사용자 정보 검색
            user = user_info.objects.get(user_id=username)

            # 비밀번호 확인
            if user.user_password == password:
                # 로그인 성공 시 세션에 사용자 정보를 저장하거나 리다이렉트
                request.session['user_id'] = user.user_id
                print('*'*50)
                messages.success(request, "로그인 성공!")
                return redirect('main_page')  # 로그인 성공 후 홈 페이지로 이동
            else:
                messages.error(request, "비밀번호가 일치하지 않습니다.")
        except user_info.DoesNotExist:
            messages.error(request, "존재하지 않는 사용자입니다.")

    return render(request, 'mainpage.html')

# ㄹㅇ 회원가입
def getUserInfo(request):
    if request.method == 'POST':    
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        # UserInfo 모델에 데이터 저장
        user_info.objects.create(
            user_id=username,
            user_password=password,
            user_email=email,
            user_name=name,
            user_phone=phone
        )
    return redirect('login_page')