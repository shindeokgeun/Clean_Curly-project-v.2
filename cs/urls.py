from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cs_index'),  # 'index'로 수정
]