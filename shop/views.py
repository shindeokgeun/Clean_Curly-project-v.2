# shop/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import QuantityForm
from carts.forms import CartAddProductForm
from reviews.models import Review 

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    categories = Category.objects.all()  # 모든 카테고리를 가져옴
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    if request.method == 'POST':
        form = QuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            # 장바구니에 수량을 업데이트 (또는 다른 로직 추가)
            # 세션에 저장하는 예시
            cart = request.session.get('cart', {})
            cart[product_id] = {
                'name': product.name,
                'quantity': quantity,
                'price': float(product.discount_price or product.price),  # Decimal을 float으로 변환
            }
            request.session['cart'] = cart

            return redirect('carts:cart_detail')  # 장바구니 페이지로 리디렉션

    else:
        form = QuantityForm()
    return render(request, 'shop/product_detail.html', {
        'product': product, 
        'form': form,
        'reviews': reviews,
        'categories': categories
    })

def product_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/product_list.html', {'category': category, 'products': products})