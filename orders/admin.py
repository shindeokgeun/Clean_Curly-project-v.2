from django.contrib import admin
from orders.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    
@admin.register(Order) #Order 모델을 장고 관리자 페이지에 등록
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'address',
                    'phone_number', 'status', 'order_date', 'updated']
    list_filter = ['status', 'order_date', 'updated']
    inlines = [OrderItemInline]