from django.contrib import admin

from .models import Coupon


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'status']
    list_filter = ['status', ]
    search_fields = ['code']


admin.site.register(Coupon, CouponAdmin)
