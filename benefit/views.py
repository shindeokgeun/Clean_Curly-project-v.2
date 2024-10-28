from django.shortcuts import render
from shop.models import Product, Category

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all() # 카테고리 추가
    return render(request, 'benefit/benefit.html', {'products': products, 'categories': categories})