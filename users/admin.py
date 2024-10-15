# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm # 사용자 생성 시 사용할 폼 지정
    form = CustomUserChangeForm # 사용자 변경 시 사용할 폼 지정
    model = CustomUser # 사용할 모델 지정
    list_display = ['username', 'email', 'is_staff', 'is_active']  # 관리자 화면에서 보여줄 사용자 리스트 항목 지정
    list_filter = ['is_staff', 'is_active'] # 리스트 필터 항목 지정 (필터링 가능한 필드)
    
    # 사용자 정보 수정 시 보여줄 필드셋 구성
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}), # 기본 필드
        ('Permissions', {'fields': ('is_staff', 'is_active')}), # 권한 관련 필드
        ('Additional Info', {'fields': ('phone_number', 'address', 'date_of_birth', 'profile_picture')}),
    )
    
    # 사용자 추가 시 보여줄 필드셋 구성
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'phone_number', 'address', 'date_of_birth', 'profile_picture', 'is_staff', 'is_active'),
        }),
    )

    search_fields = ('email', 'username') # 사용자 리스트 정렬 기준
    ordering = ('email',) # 사용자 리스트 정렬 기준
    filter_horizontal = () # 필터 옵션

admin.site.register(CustomUser, CustomUserAdmin) # CustomUser 모델을 관리자 사이트에 등록
