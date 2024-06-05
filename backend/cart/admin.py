from django.contrib import admin
from backend.enums.status import Status
from .models import Cart, CartItem, Wishlist, WishlistItem
from django.utils.html import format_html


class WishlistAdmin(admin.ModelAdmin):
    class Meta:
        model = Wishlist

    def items(self, obj):
        section = '<ol>'
        for item in obj.items.filter(status=Status.ACTIVE.value).all():
            section += '<li><a href="/admin/cart/wishlistitem/%s/change">%s</a></li>' % (item.id, item.product)
        section += '</ol>'

        return format_html(section)

    fields = ('customer', 'status', 'items')
    readonly_fields = ('customer', 'items')
    search_fields = ('customer',)

class WishlistItemsAdmin(admin.ModelAdmin):
    class Meta:
        model = WishlistItem

    fields = ('wishlist', 'product', 'status')
    search_fields = ('wishlist', 'product')
    readonly_fields = ('wishlist',)


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(WishlistItem, WishlistItemsAdmin)
