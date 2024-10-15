"""
URL configuration for myweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # 관리자 페이지 URL을 'admin/' 경로로 매핑
    path('users/', include('users.urls')),  # users 앱의 URL을 'users/' 하위 경로로 매핑
    path('', include('home.urls')),     # 홈 페이지 URL을 루트 경로로 매핑 (home 앱과 연결)
    path('cart/', include('carts.urls')), 
    path('reviews/', include('reviews.urls', namespace='reviews')),  # reviews 앱 URLs 추가
    path('shop/', include('shop.urls')),  # shop 앱 URLs 추가 (없다면)
    path('orders/', include('orders.urls', namespace='orders')),  # orders 앱 URLs 추가 (없다면)
    path('benefit/', include('benefit.urls')),
    path('cs/', include('cs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 미디어 파일을 서빙할 수 있도록 설정 (개발 환경에서만 사용)

