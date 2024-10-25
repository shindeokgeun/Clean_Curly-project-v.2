from django.contrib import admin
from .models import Report, BlockedReview

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'reason', 'created_at']
    list_filter = ['reason', 'created_at']
    search_fields = ['user__username', 'review__text', 'other_reason']

@admin.register(BlockedReview)
class BlockedReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'review']
    search_fields = ['user__username', 'review__id']