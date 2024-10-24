from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
import random

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # 전화번호 필드
    address = models.TextField(blank=True, null=True)  # 주소 필드
    date_of_birth = models.DateField(blank=True, null=True)  # 생년월일 필드
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # 프로필 사진 필드
    mileage = models.DecimalField(max_digits=10, decimal_places=2, default=5000.0)  # 기본 마일리지
    karly_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # 칼리캐시
    is_social = models.BooleanField(default=False) # 소셜 로그인 확인을 위한 필드