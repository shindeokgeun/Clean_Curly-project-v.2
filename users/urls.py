from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.login_view, name='login'),     # 로그인 페이지 urld을 views.login_view와 연결
    path('logout/', views.logout_view, name='logout'),  # 로그아웃 페이지 url을 views.logout_view와 연결 
    path('signup/', views.signup_view, name='signup'),  # 회원가입 페이지 url을 views.signup_view와 연결
    path('profile/', views.profile_view, name='profile'),  # 사용자 프로필 페이지 url을 views.profile_view와 연결
    path('profile/display/', views.profile_display_view, name='profile_display'),  # 사용자 프로필 정보를 표시하는 페이지 url을 views.profile_display_view와 연결
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('update-mileage/', views.update_mileage, name='update_mileage'),
    path('delete-mileage/', views.delete_mileage, name='delete_mileage'),
    path('profile/order-view/', views.profile_order_view, name='profile_order_view'), # 주문조회 페이지      
] 