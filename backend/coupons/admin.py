from django.contrib import admin

from .models import Coupon, CouponHistory


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'status']
    list_filter = ['status', ]
    search_fields = ['code']


class CouponHistoryAdmin(admin.ModelAdmin):
    list_display = ['coupon', 'order', 'created_at']
    list_filter = ['coupon', 'order']
    search_fields = ['coupon', 'order']
    readonly_fields = ['coupon', 'order', 'created_at']


admin.site.register(Coupon, CouponAdmin)
admin.site.register(CouponHistory, CouponHistoryAdmin)
