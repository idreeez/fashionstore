from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'price', 'quantity', 'get_cost']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'status', 'total']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'subtotal', 'discount_amount', 'total']