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
from django.db import models

@login_required
def review_entry_form(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    order_item = OrderItem.objects.filter(
        order__user=request.user,
        order__status='delivered',
        product=product,
        review__isnull=True  # 리뷰가 없는 주문 아이템만
    ).first()

    if not order_item:
        messages.error(request, "리뷰를 작성할 수 있는 상품이 아닙니다.")
        return redirect('profile_display')

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.order_item = order_item
            review.verified_purchase = True
            review.save()
            messages.success(request, '리뷰가 성공적으로 작성되었습니다.')
            return redirect('profile_display') 
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'product': product,
        'previous_page': request.META.get('HTTP_REFERER') or reverse('users:profile_display'),
    }
    return render(request, 'reviews/review_entry_form.html', context)

def product_review_section(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # 정렬 방식 파라미터 받기
    sort_type = request.GET.get('sort', 'latest')  # 기본값은 최신순
    
    # 기본 쿼리셋
    reviews = Review.objects.filter(product=product)
    
    # 정렬 적용
    if sort_type == 'helpful':
        reviews = Review.order_by_helpful(reviews)
    else:
        reviews = reviews.order_by('-created_at')
    
    # 차단된 리뷰 처리
    blocked_reviews = []
    if request.user.is_authenticated:
        blocked_reviews = BlockedReview.objects.filter(user=request.user)
        reviews = reviews.exclude(id__in=blocked_reviews.values_list('review_id', flat=True))
    
    context = {
        'product': product,
        'reviews': reviews,
        'user': request.user,
        'current_sort': sort_type,
        'blocked_reviews': blocked_reviews.values_list('review_id', flat=True) if request.user.is_authenticated else []
    }
    return render(request, 'reviews/product_review_section.html', context)

@login_required
def review_mypage(request):
    user = request.user
    written_reviews = Review.objects.filter(user=user).order_by('-created_at')
    
    writeable_items = OrderItem.objects.filter(
        order__user=user,
        order__status='delivered'
    ).exclude(
        review__isnull=False  # 이미 리뷰가 있는 주문 아이템 제외
    )

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


@login_required
def rate_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    user = request.user
    action = request.POST.get('action')

    current_sort = request.GET.get('sort', 'latest')
    
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
    return redirect(f"{reverse('shop:product_detail', args=[review.product.id])}?sort={current_sort}")


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
            
            # 디버깅 출력
            print(f"Report submission - User: {request.user.username}, Review ID: {review_id}")
            print(f"Reason: {reason}, Block User: {block_user}")

            # 신고 생성
            report = Report(
                user=request.user, 
                review=review, 
                reason=reason,
                block_user=block_user
            )
            
            if reason == 'other':
                report.other_reason = other_reason
            
            report.save()
            print(f"Report saved with ID: {report.id}")

            if block_user:
                try:
                    # 리뷰 차단 구현
                    blocked, created = BlockedReview.objects.get_or_create(
                        user=request.user,
                        review=review,  # review_id가 아닌 review 객체 사용
                        defaults={'created_at': timezone.now()}
                    )
                    print(f"BlockedReview {'created' if created else 'already exists'} - User: {request.user.id}, Review: {review_id}")
                    
                    if created:
                        messages.success(request, '해당 리뷰가 차단되었습니다.')
                    else:
                        messages.info(request, '이미 차단된 리뷰입니다.')
                except Exception as e:
                    print(f"Error creating BlockedReview: {str(e)}")
                    messages.error(request, '리뷰 차단 중 오류가 발생했습니다.')

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