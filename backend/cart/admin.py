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


class CartAdmin(admin.ModelAdmin):
    class Meta:
        model = Cart

    def items(self, obj):
        section = '<ol>'
        for item in obj.items.filter(status=Status.ACTIVE.value).all():
            section += '<li><a href="/admin/cart/cartitem/%s/change">%s</a></li>' % (item.id, item.product)
        section += '</ol>'

        return format_html(section)

    fields = ('customer', 'status', 'items', 'total_price', 'subtotal_price', 'total_items', 'discount')
    readonly_fields = ('customer', 'items', 'total_price', 'subtotal_price', 'total_items', 'discount')


class CartItemAdmin(admin.ModelAdmin):
    class Meta:
        model = CartItem

    def total_price(self, obj):
        return obj.quantity * obj.product.selling_price

    def price(self, obj):
        return obj.product.selling_price

    fields = ('cart', 'product', 'quantity', 'status', 'price', 'total_price')
    search_fields = ('cart', 'product')
    readonly_fields = ('cart', 'total_price', 'price',)


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(WishlistItem, WishlistItemsAdmin)
