from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'valid_from', 'valid_to', 'active', 'is_valid')
    list_filter = ('active', 'valid_from', 'valid_to')
    search_fields = ('code',)
    date_hierarchy = 'valid_from'
    
    fieldsets = (
        (None, {
            'fields': ('code', 'discount', 'active')
        }),
        ('Срок действия', {
            'fields': ('valid_from', 'valid_to'),
            'classes': ('wide',)
        }),
    )