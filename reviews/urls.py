from django.urls import path
from . import views

app_name = 'reviews'  # URL 네임스페이스 추가

urlpatterns = [
    # 리뷰 작성 및 조회
    path('review/entry/<int:product_id>/', views.review_entry_form, name='review_entry_form'),
    path('product/<int:product_id>/reviews/', views.product_review_section, name='product_review_section'),
    
    # 마이페이지 관련
    path('mypage/reviews/', views.review_mypage, name='review_mypage'),
    
    # 리뷰 수정/삭제
    path('review/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    
    # 리뷰 평가
    path('reviews/<int:review_id>/rate/', views.rate_review, name='rate_review'),
    
    # 신고 및 차단 관련
    path('report/<int:review_id>/', views.report_review, name='report_review'),
    path('reports/', views.report_list, name='report_list'),
    path('review/unblock/<int:review_id>/', views.unblock_review, name='unblock_review'),
    
    # 디버그
    path('debug/', views.debug_view, name='debug_view'),

    # 고객센터 탭
    path('report/list/', views.report_list, name='report_list'),
]