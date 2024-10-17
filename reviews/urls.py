from django.urls import path
from . import views

app_name = 'reviews'  # URL 네임스페이스 추가

urlpatterns = [
    path('review/entry/<int:product_id>/', views.review_entry_form, name='review_entry_form'),
    path('product/<int:product_id>/reviews/', views.product_review_section, name='product_review_section'),
    path('mypage/reviews/', views.review_mypage, name='review_mypage'),
    path('review/edit/<int:review_id>/', views.edit_review, name='edit_review'),  # 리뷰 수정
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),  # 리뷰 삭제
    path('debug/', views.debug_view, name='debug_view'),
    path('edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
]