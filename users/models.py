from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from shop.models import Product

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True) # 전화번호 필드, 최대 15자리 제한
    address = models.TextField(blank=True, null=True) # 주소 필드, 텍스트형식
    date_of_birth = models.DateField(blank=True, null=True) # 생년월일 필드 , 날짜형식
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) # 프로필 사진 필드, 이미지파일 'profile_pics/' 디렉토리에 업로드
    mileage = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # 마일리지 필드
    karly_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # 칼리캐시 필드

