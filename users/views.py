from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from django.contrib.auth import authenticate
from reviews.views import get_review_data

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