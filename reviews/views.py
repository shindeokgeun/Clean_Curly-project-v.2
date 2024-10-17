from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from shop.models import Product
from orders.models import Order, OrderItem
from .forms import ReviewForm
from .models import Review
from django.http import HttpResponse
from django.core.files.base import ContentFile

@login_required
def review_entry_form(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    previous_page = request.META.get('HTTP_REFERER') or reverse('users:profile_display')

    # 해당 상품에 대한 배송 완료된 주문이 있는지 확인
    if not Order.objects.filter(user=request.user, items__product=product, status='delivered').exists():
        messages.error(request, "리뷰를 작성할 수 있는 상품이 아닙니다.")
        return redirect('profile_display') 

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.verified_purchase = True
            review.save()
            messages.success(request, '리뷰가 성공적으로 작성되었습니다.')
            return redirect('profile_display') 
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'product': product,
        'previous_page': previous_page,
    }
    return render(request, 'reviews/review_entry_form.html', context)

def product_review_section(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    context = {
        'product': product,
        'reviews': reviews,
    }
    return render(request, 'reviews/product_review_section.html', context)

@login_required
def review_mypage(request):
    user = request.user
    written_reviews = Review.objects.filter(user=user).order_by('-created_at')
    
    eligible_orders = Order.objects.filter(user=user, status='delivered')
    writeable_items = OrderItem.objects.filter(order__in=eligible_orders)
    
    reviewed_products = Review.objects.filter(user=user).values_list('product', flat=True)
    writeable_items = writeable_items.exclude(product__in=reviewed_products)
    
    review_data = {
        'written_reviews': written_reviews,
        'writeable_items': writeable_items,
    }
    
    return render(request, 'reviews/review_mypage.html', {'review_data': review_data})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                image_content = ContentFile(image_file.read())
                review.image.save(image_file.name, image_content, save=False)
            elif form.cleaned_data['image'] is False:
                review.image = None
            review.save()
            messages.success(request, '리뷰가 성공적으로 수정되었습니다.')
            return redirect('profile_display')
        else:
            messages.error(request, '폼 유효성 검사 실패')
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'review': review,
    }
    return render(request, 'reviews/edit_review.html', context)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        messages.success(request, '리뷰가 성공적으로 삭제되었습니다.')
    return redirect('profile_display')


def debug_view(request):
    return HttpResponse("Debug view is working!")


def get_review_data(user):
    written_reviews = Review.objects.filter(user=user).order_by('-created_at')
    
    eligible_orders = Order.objects.filter(user=user, status='delivered')
    writeable_items = OrderItem.objects.filter(order__in=eligible_orders)
    
    reviewed_products = Review.objects.filter(user=user).values_list('product', flat=True)
    writeable_items = writeable_items.exclude(product__in=reviewed_products)
    
    return {
        'written_reviews': written_reviews,
        'writeable_items': writeable_items,
    }
