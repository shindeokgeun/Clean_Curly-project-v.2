# shop/urls.py
from django.urls import path, include
from . import views
app_name = 'shop'
urlpatterns = [

    path('product/<int:product_id>/', views.product_detail, name='product_detail'), # 동적 상품 페이지
    path('category/<int:category_id>/', views.product_by_category, name='product_by_category'), #카테고리별 상품 목록
    ########## 상품 등록 ##########
    path('product/manage/', views.product_manage, name='product_manage'),  # 상품 관리 페이지
    path('product-register/', views.product_register, name='product_register'),
    path('success/', views.success_page, name='success_page'),  # 성공 페이지 추가

    path('product/<int:product_id>/update/', views.product_update, name='product_update'),
    path('product/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('seller/purchase-history/', views.purchase_history, name='purchase_history'),
]