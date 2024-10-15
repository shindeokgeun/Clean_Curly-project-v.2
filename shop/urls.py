# shop/urls.py
from django.urls import path, include
from . import views
app_name = 'shop'
urlpatterns = [

    path('product/<int:product_id>/', views.product_detail, name='product_detail'), # 동적 상품 페이지
    path('category/<int:category_id>/', views.product_by_category, name='product_by_category'), #카테고리별 상품 목록
    
]