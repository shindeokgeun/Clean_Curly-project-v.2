from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from shop.models import Product
from orders.models import Order, OrderItem
from .forms import ReviewForm, ReportForm
from .models import Review, Report, BlockedReview
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Report
from django.utils import timezone

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
    print(f"Initial reviews count: {reviews.count()}")  # 디버깅 출력

    blocked_reviews = []
    if request.user.is_authenticated:
        # 차단한 리뷰 확인
        blocked_reviews = list(BlockedReview.objects.filter(
            user=request.user
        ).values_list('review', flat=True))
        print(f"Found blocked reviews: {blocked_reviews}")  # 디버깅 출력
        
        reviews = reviews.exclude(id__in=blocked_reviews)
        print(f"Reviews count after excluding blocked: {reviews.count()}")  # 디버깅 출력

  #  if request.user.is_authenticated:
  #      # 차단한 리뷰 제외
  #      blocked_reviews = BlockedReview.objects.filter(
  #          user=request.user
  #      ).values_list('review', flat=True)
  #      reviews = reviews.exclude(id__in=blocked_reviews)
    
    context = {
        'product': product,
        'reviews': reviews,
        'user': request.user,
        'blocked_reviews': blocked_reviews,  # 템플릿에 전달
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


@login_required
def rate_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    user = request.user
    action = request.POST.get('action')
    
    if action == 'helpful':
        if user in review.unhelpful_users.all():
            review.unhelpful_users.remove(user)
            review.unhelpful_count = max(0, review.unhelpful_count - 1)
        if user in review.helpful_users.all():
            review.helpful_users.remove(user)
            review.helpful_count = max(0, review.helpful_count - 1)
        else:
            review.helpful_users.add(user)
            review.helpful_count += 1
    elif action == 'unhelpful':
        if user in review.helpful_users.all():
            review.helpful_users.remove(user)
            review.helpful_count = max(0, review.helpful_count - 1)
        if user in review.unhelpful_users.all():
            review.unhelpful_users.remove(user)
            review.unhelpful_count = max(0, review.unhelpful_count - 1)
        else:
            review.unhelpful_users.add(user)
            review.unhelpful_count += 1
    
    review.save()
    return redirect(reverse('shop:product_detail', args=[review.product.id]))


@login_required
def report_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    product_url = reverse('shop:product_detail', args=[review.product.id])

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            other_reason = form.cleaned_data['other_reason']
            block_user = form.cleaned_data['block_user']
            
            # 디버깅 출력 추가
            print(f"Report submission - Reason: {reason}, Block User: {block_user}")

            # 신고 생성
            report = Report(
                user=request.user, 
                review=review, 
                reason=reason,
                block_user=block_user  # block_user 상태 저장
            )
            
            if reason == 'other':
                report.other_reason = other_reason
            
            report.save()
            print(f"Report saved with ID: {report.id}")  # 디버깅 출력

            if block_user:
                # 리뷰 차단 구현
              #  BlockedReview.objects.get_or_create(
              #      user=request.user,
              #      review=review,
              #      defaults={'created_at': timezone.now()}
              #  )
              #  messages.success(request, '해당 리뷰가 차단되었습니다.') 
                print(f"Attempting to create BlockedReview - User: {request.user.id}, Review: {review.id}")
                blocked, created = BlockedReview.objects.get_or_create(
                    user=request.user,
                    review=review,
                    defaults={'created_at': timezone.now()}
                )
                print(f"BlockedReview {'created' if created else 'already exists'}")  # 디버깅 출력
                messages.success(request, '해당 리뷰가 차단되었습니다.')

            messages.success(request, '신고가 접수되었습니다.')
            return redirect('shop:product_detail', product_id=review.product.id)
    else:
        form = ReportForm()
    
    context = {
        'form': form,
        'review': review,
        'product_url': product_url,
    }
    return render(request, 'reviews/report_review.html', context)

@staff_member_required
def report_list(request):
    reports = Report.objects.all().order_by('-created_at')
    context = {
        'reports': reports,
    }
    return render(request, 'reviews/report_list.html', context)

# 차단 해제 기능 추가 (선택사항)
@login_required
def unblock_review(request, review_id):
    blocked_review = get_object_or_404(
        BlockedReview, 
        user=request.user, 
        review_id=review_id
    )
    review_product_id = blocked_review.review.product.id
    blocked_review.delete()
    messages.success(request, '리뷰 차단이 해제되었습니다.')
    return redirect('shop:product_detail', product_id=review_product_id)