from django.shortcuts import render
from shop.models import Product, Category

# Create your views here.

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all() # 카테고리 추가
    return render(request, 'cs/cs.html', {'products': products, 'categories': categories})

def review_report(request):
    return render(request, 'reviews/report_list.html')