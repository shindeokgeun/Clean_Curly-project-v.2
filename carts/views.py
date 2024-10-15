from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from carts.cart import Cart
from shop.models import Product
from carts.forms import CartAddProductForm

@require_POST #post요청만 허용하도록 강제
def cart_add(request, product_id):
    cart = Cart(request) #현재 사용자 세션에 있는 장바구니를 가져오거나 새로운 장바구니 객체를 생성하여 cart에 저장
    product = get_object_or_404(Product, id=product_id) #Product에서 product_id에 해당하는 상품 가져옴
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('carts:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('carts:cart_detail')


def cart_detail(request): #장바구니의 상세내용을 보여줌
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    return render(request, 'carts/cart.html', {'cart':cart})


def cart_cart(request): #장바구니 페이지를 보여줌
    return render(request, 'carts/cart.html')


