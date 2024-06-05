from django.contrib import admin

from .models import Cart, CartItem, Wishlist, WishlistItem
from django.utils.html import format_html


class WishlistAdmin(admin.ModelAdmin):
    class Meta:
        model = Wishlist

    def items(self, obj):
        section = '<ol>'
        for item in obj.items.all():
            section += '<li><a href="/admin/cart/wishlistitem/%s/change">%s</a></li>' % (item.id, item.product)
        section += '</ol>'

        return format_html(section)

    fields = ('customer', 'status', 'items')
    readonly_fields = ('customer', 'items')
    search_fields = ('customer',)


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(WishlistItem)
