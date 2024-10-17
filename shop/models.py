from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    # 필수 필드
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    
    # 필수 정보 필드 (기본값 설정)
    shipping_info = models.CharField(max_length=200, default="배송 정보 입력")
    seller = models.CharField(max_length=200, default="판매자 입력")
    packaging_type = models.CharField(max_length=200, default="포장 타입 입력")

    # 선택적 정보 필드 (nullable=True)
    sales_unit = models.CharField(max_length=100, blank=True, null=True)  # 판매단위
    weight_volume = models.CharField(max_length=100, blank=True, null=True)  # 중량/용량
    expiration_date = models.TextField(blank=True, null=True)  # 소비기한 또는 유통기한
    Notice_info = models.TextField(blank=True, null=True) # 안내 사항
    allergy_info = models.TextField(blank=True, null=True)  # 알레르기 정보
    livestock_trace_info = models.CharField(max_length=200, blank=True, null=True)  # 축산물 이력정보


    def __str__(self):
        return self.name

    @property
    def discount_percentage(self):
        """할인율 계산 (정가 대비 할인가)"""
        if self.discount_price and self.price > 0:
            return round((self.price - self.discount_price) / self.price * 100)
        return 0  # 할인 가격이 없을 경우 0%


