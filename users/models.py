from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True) # 전화번호 필드, 최대 15자리 제한
    address = models.TextField(blank=True, null=True) # 주소 필드, 텍스트형식
    date_of_birth = models.DateField(blank=True, null=True) # 생년월일 필드 , 날짜형식
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) # 프로필 사진 필드, 이미지파일 'profile_pics/' 디렉토리에 업로드
