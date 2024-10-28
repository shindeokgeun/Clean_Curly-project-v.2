from django.db import models
from django.conf import settings


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='reviews')
    order_item = models.OneToOneField('orders.OrderItem', on_delete=models.SET_NULL, null=True, related_name='review')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='review_images/', blank=True, null=True)
    verified_purchase = models.BooleanField(default=False)
    helpful_count = models.PositiveIntegerField(default=0)
    unhelpful_count = models.PositiveIntegerField(default=0)
    helpful_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='helpful_reviews', blank=True)
    unhelpful_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='unhelpful_reviews', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"

    @classmethod
    def create_review(cls, user, product, rating, text, image=None):
        verified = cls.verify_purchase(user, product)
        return cls.objects.create(
            user=user, 
            product=product, 
            rating=rating, 
            text=text, 
            image=image, 
            verified_purchase=verified
        )

    @staticmethod
    def verify_purchase(user, product):
        # 이 메서드는 나중에 실제 구매 확인 로직으로 대체.
        return Purchase.objects.filter(user=user, product=product).exists()

    @classmethod
    def order_by_helpful(cls, queryset):
        return queryset.annotate(
            help_count=models.Count('helpful_users')
        ).order_by('-help_count', '-created_at')

class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reports')
    reason = models.CharField(max_length=100)
    other_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # 새로 추가할 필드들
    block_user = models.BooleanField(default=False)  # 사용자 차단 여부
    processed = models.BooleanField(default=False)   # 신고 처리 상태
    processed_at = models.DateTimeField(null=True, blank=True)  # 처리된 시간
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='processed_reports'
    )  # 처리한 관리자

    class Meta:
        ordering = ['-created_at']  # 최신 신고순으로 정렬

    def __str__(self):
        return f"Report by {self.user.username} for review {self.review.id}"

    def mark_as_processed(self, admin_user):
        """신고를 처리 완료로 표시"""
        from django.utils import timezone
        self.processed = True
        self.processed_at = timezone.now()
        self.processed_by = admin_user
        self.save()

class BlockedReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blocked_reviews')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='blocked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')  # 동일한 리뷰를 중복 차단 방지

    def __str__(self):
        return f"{self.user.username} blocked review {self.review.id}"
    

