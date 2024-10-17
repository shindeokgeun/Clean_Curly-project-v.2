from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from django.contrib.auth import authenticate
from reviews.views import get_review_data
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.contrib.auth import update_session_auth_hash

# 로그인 뷰
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # 폼에서 인증된 사용자 가져오기
            auth_login(request, user)  # 로그인 처리
            return redirect('index')  # 로그인 후 홈 페이지로 리디렉션
    else:
        form = CustomAuthenticationForm()  # GET 요청 시 빈 폼 생성
    return render(request, 'users/마켓_로그인.html', {'form': form})  # 로그인 템플릿 렌더링


# 로그아웃 뷰
def logout_view(request):
    auth_logout(request)  # 로그아웃 처리
    return redirect('index')  # 로그아웃 후 홈 페이지로 리디렉션

# 회원가입 뷰
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # 사용자 등록 폼에 POST 데이터 및 파일 처리
        if form.is_valid():
            user = form.save()  # 유저 정보 저장
            auth_login(request, user)  # 회원가입 후 자동 로그인
            return redirect('index')  # 가입 후 홈 페이지로 리디렉션
    else:
        form = CustomUserCreationForm()  # GET 요청 시 빈 폼 생성
    return render(request, 'users/마켓_회원가입.html', {'form': form})  # 회원가입 템플릿 렌더링

# 마켓 메인 페이지 뷰
def market_view(request):
    # 사용자 정보를 템플릿에 전달
    context = {
        'user': request.user,
    }
    return render(request, 'market.html', context)  # 마켓 메인 페이지 렌더링

# 개인 페이지 뷰 (로그인 필요)
@login_required
def profile_view(request):
    if request.method == 'POST':
        # 비밀번호 확인 처리
        if 'confirm_password' in request.POST:
            password = request.POST.get('confirm_password')  # 입력된 비밀번호 가져오기
            user = authenticate(username=request.user.username, password=password)  # 비밀번호 확인
            if user is not None:
                return redirect('profile_display')  # 비밀번호가 일치하면 프로필 디스플레이 페이지로 이동
            else:
                return render(request, 'users/personal_page.html', {'error': '비밀번호가 일치하지 않습니다.'})
        else:
            # 사용자 정보 수정 처리
            form = CustomUserChangeForm(request.POST, instance=request.user, files=request.FILES)
            if form.is_valid():
                form.save()  # 사용자 정보 저장
                return redirect('profile')  # 수정 후 다시 프로필 페이지로 리디렉션
    else:
        if 'password_confirmed' in request.GET:
            return redirect('profile_display')  # 비밀번호 확인이 완료되면 프로필 디스플레이 페이지로 이동
        return render(request, 'users/personal_page.html')  # 비밀번호 확인 페이지 렌더링

# 프로필 디스플레이 뷰 (로그인 필요)
@login_required
def profile_display_view(request):
    review_data = get_review_data(request.user)
    context = {
        'user': request.user,
        'review_data': review_data,
    }
    return render(request, 'users/profile_display.html', context)


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
from .forms import ProfileUpdateForm

@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)

        # 현재 비밀번호 확인
        current_password = request.POST.get('current_password')
        if not check_password(current_password, user.password):
            form.add_error('current_password', '현재 비밀번호가 올바르지 않습니다.')
        else:
            if form.is_valid():
                # 비밀번호가 입력된 경우
                if form.cleaned_data['password']:
                    user.set_password(form.cleaned_data['password'])  # 비밀번호 해싱
                form.save()
                update_session_auth_hash(request, user)  # 세션 업데이트
                return redirect('profile_display')  # 수정 완료 후 리다이렉트할 페이지
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'users/profile_display_change.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser  # 사용자 모델을 임포트하세요

@login_required
def update_mileage(request):
    if request.method == 'POST':
        mileage = int(request.POST.get('mileage', 0))
        karly_cash = int(request.POST.get('karly_cash', 0))

        user = request.user
        user.mileage += mileage  # 기존 적립금에 추가
        user.karly_cash += karly_cash  # 기존 칼리캐시에 추가
        user.save()  # 변경사항 저장

        return redirect('http://127.0.0.1:8000/users/profile/display/')  # 업데이트 후 프로필 페이지로 리디렉션

    return render(request, 'users/update_mileage.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser  # 필요에 따라 모델 import
from django.contrib import messages

@login_required
def delete_mileage(request):
    if request.method == 'POST':
        # 폼에서 삭제할 금액 입력받기
        mileage_to_delete = int(request.POST.get('mileage', 0))
        karly_cash_to_delete = int(request.POST.get('karly_cash', 0))
        
        # 현재 사용자 정보 가져오기
        user = request.user

        # 적립금 삭제 로직
        if mileage_to_delete <= user.mileage:
            user.mileage -= mileage_to_delete
        else:
            messages.error(request, '적립금은 0원 이하로 내려갈 수 없습니다.')
            return redirect('delete_mileage')  # 다시 삭제 페이지로 리다이렉트

        # 칼리캐시 삭제 로직
        if karly_cash_to_delete <= user.karly_cash:
            user.karly_cash -= karly_cash_to_delete
        else:
            messages.error(request, '칼리캐시는 0원 이하로 내려갈 수 없습니다.')
            return redirect('delete_mileage')  # 다시 삭제 페이지로 리다이렉트

        user.save()
        messages.success(request, '적립금 및 칼리캐시가 성공적으로 업데이트되었습니다.')
        return redirect('http://127.0.0.1:8000/users/profile/display/')  # 적절한 리다이렉트 경로로 변경

    return render(request, 'users/delete_mileage.html')  # 삭제 페이지 템플릿