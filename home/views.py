from django.shortcuts import render
from datetime import datetime, timedelta
from django.utils.timezone import now
from shop.models import Product, Category


def index(request):
    # Product 모델에서 모든 상품을 가져와서 템플릿에 전달
    products = Product.objects.all()
    categories = Category.objects.all() # 카테고리 추가
    return render(request, 'home/market.html', {'products': products, 'categories': categories})


def special_offers_view(request):
    current_time = now()
    # 자정 시간을 설정 (오늘 자정 기준으로 계산)
    midnight = current_time.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    # 자정까지 남은 시간 계산
    time_remaining = midnight - current_time
    
    # 초 단위로 전달
    return render(request, 'special_offers.html', {'time_remaining_seconds': int(time_remaining.total_seconds())})

