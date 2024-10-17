from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),  
    path('users/', include('users.urls')),  # users 앱의 URL을 'users/' 하위 경로로 매핑

]
