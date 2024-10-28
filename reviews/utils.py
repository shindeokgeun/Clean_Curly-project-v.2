def get_review_data(user):
    from .models import Review
    from orders.models import OrderItem

    written_reviews = Review.objects.filter(user=user).order_by('-created_at')
    
    writeable_items = OrderItem.objects.filter(
        order__user=user,
        order__status='delivered'
    ).exclude(
        review__isnull=False
    )
    
    return {
        'written_reviews': written_reviews,
        'writeable_items': writeable_items,
    }