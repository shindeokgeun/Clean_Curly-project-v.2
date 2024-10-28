from django.db import migrations

def link_reviews_to_order_items(apps, schema_editor):
    Review = apps.get_model('reviews', 'Review')
    OrderItem = apps.get_model('orders', 'OrderItem')
    
    for review in Review.objects.filter(order_item__isnull=True):
        # 해당 상품의 가장 오래된 배송완료 주문 찾기
        order_item = OrderItem.objects.filter(
            order__user=review.user,
            product=review.product,
            order__status='delivered',
            review__isnull=True
        ).first()
        
        if order_item:
            review.order_item = order_item
            review.save()

def reverse_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('reviews', '0007_review_order_item'),  # 이전 마이그레이션 파일명
    ]

    operations = [
        migrations.RunPython(link_reviews_to_order_items, reverse_func),
    ]