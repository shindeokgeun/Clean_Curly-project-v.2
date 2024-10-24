from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model  # CustomUser를 동적으로 가져오기 위해
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm, ProfileUpdateForm
from .models import CustomUser  # 필요에 따라 모델 import
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
from django.contrib.auth import login as auth_login, authenticate

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # 사용자 인증 후 로그인 (백엔드를 명시적으로 지정)
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/마켓_회원가입.html', {'form': form})

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


# 마일리지(적립금, 컬리캐쉬) 추가 뷰
@login_required
def update_mileage(request):
    if request.method == 'POST':
        mileage = int(request.POST.get('mileage', 0))
        karly_cash = int(request.POST.get('karly_cash', 0))

        user = request.user
        user.mileage += mileage  # 기존 적립금에 추가
        user.karly_cash += karly_cash  # 기존 칼리캐시에 추가
        user.save()  # 변경사항 저장
        messages.success(request, '적립금 및 컬리캐시가 성공적으로 업데이트되었습니다.')
        return redirect('http://127.0.0.1:8000/users/profile/display/')  # 업데이트 후 프로필 페이지로 리디렉션

    return render(request, 'users/update_mileage.html')


# 마일리지(적립금, 컬리캐쉬 관련) 삭제 뷰
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

        # 컬리캐시 삭제 로직
        if karly_cash_to_delete <= user.karly_cash:
            user.karly_cash -= karly_cash_to_delete
        else:
            messages.error(request, '컬리캐시는 0원 이하로 내려갈 수 없습니다.')
            return redirect('delete_mileage')  # 다시 삭제 페이지로 리다이렉트

        user.save()
        messages.success(request, '적립금 및 컬리캐시가 성공적으로 업데이트되었습니다.')
        return redirect('http://127.0.0.1:8000/users/profile/display/')  # 적절한 리다이렉트 경로로 변경

    return render(request, 'users/delete_mileage.html')  # 삭제 페이지 템플릿


# 아이디 찾기 뷰
def find_username(request):
    User = get_user_model()  # CustomUser 모델 가져오기
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)  # CustomUser로 변경
            # 아이디를 이메일로 전송
            send_mail(
                'Your Username',
                f'Your username is: {user.username}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            # 이메일 전송 후 로그인 페이지로 리다이렉트
            return redirect('login')  # 'login'은 URLconf에서 정의된 로그인 URL의 이름입니다.
        except User.DoesNotExist:
            return render(request, 'users/find_username.html', {'error': 'Email not found.'})

    return render(request, 'users/find_username.html')

# 비밀번호 찾기 뷰
def reset_password(request):
    User = get_user_model()  # CustomUser 모델 가져오기
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)  # CustomUser로 변경
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            link = request.build_absolute_uri(f'/users/reset-password-confirm/{uid}/{token}/')

            # 비밀번호 재설정 링크를 이메일로 전송
            send_mail(
                'Reset your password',
                f'Click the link to reset your password: {link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return redirect('login')  # 로그인 페이지로 리다이렉트
        except User.DoesNotExist:
            return render(request, 'users/reset_password.html', {'error': 'Email not found.'})
        except Exception as e:
            return render(request, 'users/reset_password.html', {'error': 'Failed to send email. Please try again.'})

    return render(request, 'users/reset_password.html')



# 비밀번호 재설정 확인 뷰
import logging

logger = logging.getLogger(__name__)

def reset_password_confirm(request, uidb64, token):
    logger.info("Attempting to render reset_password_confirm.html")
    User = get_user_model()  # CustomUser 모델 가져오기
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        logger.warning(f"Invalid UID: {uidb64}, Token: {token}")
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')  # 로그인 페이지로 리디렉션
        else:
            form = SetPasswordForm(user)
    else:
        form = None  # 유효하지 않은 사용자이거나 토큰인 경우 None 설정
    logger.info("Rendering reset_password_confirm.html")
    return render(request, 'users/reset_password_confirm.html', {'form': form})

# 주문조회
from orders.models import Order, OrderItem 

@login_required
def profile_order_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')   
    return render(request,'users/profile_order_view.html', {'orders' : orders})


@login_required
def delete_account(request):
    if request.method == 'POST':
        # 사용자가 비밀번호를 입력했는지 확인
        if request.user.check_password(request.POST['password']):
            # 사용자 계정을 삭제합니다
            user = request.user
            user.delete()  # 계정 삭제
            messages.success(request, '계정이 성공적으로 삭제되었습니다.')
            return redirect('index')  
        else:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
    
    return render(request, 'users/delete_account.html')


# 구글 로그인 비밀번호 설정뷰
from django.contrib.auth.hashers import make_password

# @login_required
# def set_password(request):
#     if request.method == "POST":
#         password = request.POST.get("password")
#         user = request.user
#         if password:  # 비밀번호가 비어있지 않은지 확인
#             user.password = make_password(password)
#             user.save()
#             messages.success(request, "비밀번호가 성공적으로 설정되었습니다.")
#             return redirect("index")  # 비밀번호 설정 후 리디렉션할 URL
#         else:
#             messages.error(request, "비밀번호를 입력해주세요.")
#     return render(request, "users/set_password.html")

# http://127.0.0.1:8000/users/set-password/ 에서 비밀번호 지정해줘야함.

@login_required
def set_password(request):
    if request.user.social_auth.exists():  # 소셜 로그인 여부 확인
        if request.method == 'POST':
            form = SetPasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # 비밀번호 변경 후 세션 업데이트
                return redirect('index')  # 비밀번호 설정 후 리디렉션할 URL
        else:
            form = SetPasswordForm(user=request.user)
        
        return render(request, 'users/set_password.html', {'form': form}) # 소셜 로그인 계정 (즉, 비밀번호가 등록이 안되어 있는 분들은 비밀번호 설정 페이지로 이동)
    
    # 소셜 로그인 계정이 아닌 경우에는 403 Forbidden 응답을 반환 (기존 회원가입하신분들, 즉 비밀번호가 있는 분들은 403에러 페이지로 이동)
    return render(request, '403.html', status=403)