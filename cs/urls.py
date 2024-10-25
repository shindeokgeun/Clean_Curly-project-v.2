from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cs_index'),  # 'index'로 수정
    path('report-review/', views.review_report, name='report_review'),
]