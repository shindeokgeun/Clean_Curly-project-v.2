# shop/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import QuantityForm
from carts.forms import CartAddProductForm
from reviews.models import Review, BlockedReview
from .forms import ProductForm
from django.http import HttpResponseForbidden
from reviews.views import product_review_section  # 추가
from django.template.response import SimpleTemplateResponse  # 추가
from django.db import models

#### 상품 상세정보 페이지 ####
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    categories = Category.objects.all()
   
    sort_type = request.GET.get('sort', 'latest')
    
    # 리뷰 정렬
    reviews = Review.objects.filter(product=product)
    if sort_type == 'helpful':
        reviews = reviews.annotate(
            help_count=models.Count('helpful_users')
        ).order_by('-help_count', '-created_at')
    else:
        reviews = reviews.order_by('-created_at')
    
    # 리뷰 차단 관련 데이터 추가
    blocked_reviews = []
    if request.user.is_authenticated:
        blocked_reviews = list(BlockedReview.objects.filter(
            user=request.user
        ).values_list('review_id', flat=True))
        reviews = reviews.exclude(id__in=blocked_reviews)
    
    if request.method == 'POST':
        form = QuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart = request.session.get('cart', {})
            cart[product_id] = {
                'name': product.name,
                'quantity': quantity,
                'price': float(product.discount_price or product.price),
            }
            request.session['cart'] = cart
            return redirect('carts:cart_detail')
    else:
        form = QuantityForm()

    context = {
        'product': product, 
        'form': form,
        'reviews': reviews,
        'categories': categories,
        'blocked_reviews': blocked_reviews,  # 차단된 리뷰 ID 목록 추가
        'user': request.user,  # user 정보 추가
        'current_sort': sort_type,  # 정렬 상태 추가
    }
    return render(request, 'shop/product_detail.html', context)


def product_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/product_list.html', {'category': category, 'products': products})



########## 고객센터 -> 상품 관리 기능 구현 ##########
from django.contrib.auth.decorators import user_passes_test

def product_manage(request):
    if not is_seller(request.user):  # 판매자 여부 확인
        return HttpResponseForbidden(render(request, 'shop/403.html'))  # 403 페이지 렌더링

    products = Product.objects.all() # 상품 등록 관리자가 한명이라 다 불러오는 걸로.. 
    return render(request, 'shop/product_manage.html', {'products': products})



# 판매자 여부를 확인하는 함수
def is_seller(user):
    return user.groups.filter(name='판매자').exists()

# 상품 등록 페이지 뷰

def product_register(request):
    if not is_seller(request.user):  # 권한이 없으면 403 페이지 렌더링
        return HttpResponseForbidden(render(request, 'shop/403.html'))
    
    categories = Category.objects.all()  # 모든 카테고리를 가져옴
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # 폼 데이터와 파일 데이터 처리
        if form.is_valid():
            form.save()  # 폼 데이터가 유효하면 저장
            return redirect('/shop/success/')  # 성공 시 리디렉션 (적절한 URL로 수정 필요)
    else:
        form = ProductForm()

    return render(request, 'shop/product_register.html', {'categories': categories, 'form': form})


def success_page(request):
    return redirect('index')

#### 상품 수정 기능 ####
def product_update(request, product_id):
    if not is_seller(request.user):  # 판매자 여부 확인
        return HttpResponseForbidden(render(request, 'shop/403.html'))  # 403 페이지 렌더링


    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)  # instance를 사용해 수정
        if form.is_valid():
            form.save()  # 수정된 내용을 저장
            return redirect('shop:product_detail', product_id=product.id)  # 수정 후 상세 페이지로 리디렉션
    else:
        form = ProductForm(instance=product)  # 기존 상품 데이터를 폼에 미리 채워줌

    return render(request, 'shop/product_update.html', {'form': form})

#### 상품 삭제 기능 ####
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # 판매자 여부를 확인하여 권한 없는 사용자 차단
    if not is_seller(request.user):
        return HttpResponseForbidden(render(request, 'shop/403.html'))  # 403 페이지 렌더링

    if request.method == 'POST':
        product.delete()  # 상품 삭제
        return redirect('shop:product_manage')  # 삭제 후 목록 페이지로 리디렉션

    return render(request, 'shop/product_delete.html', {'product': product})


### 구매자별 구매 이력 조회 ###
from django.contrib.auth.decorators import login_required
from orders.models import OrderItem

@login_required
def purchase_history(request):
    # 판매자인지 확인
    if not is_seller(request.user):
        return HttpResponseForbidden("접근 권한이 없습니다.")  # 권한이 없으면 403 Forbidden 응답

    # 모든 구매 이력을 가져옵니다.
    purchase_history = OrderItem.objects.select_related('order', 'product')

    # 구매자별로 이력을 그룹화
    grouped_by_buyer = {}
    for item in purchase_history:
        buyer = item.order.user
        if buyer not in grouped_by_buyer:
            grouped_by_buyer[buyer] = []
        grouped_by_buyer[buyer].append(item)

    context = {
        'purchase_history': grouped_by_buyer,
    }
    return render(request, 'shop/purchase_history.html', context)