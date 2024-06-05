from .models import Cart, CartItem, Wishlist, WishlistItem
from rest_framework import serializers


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('key', 'created_at', 'updated_at', 'customer', 'total_price', 'subtotal_price',
                  'total_items', 'discount', 'tax', 'shipping', 'total', 'address', 'status')
        read_only_fields = ('key', 'created_at')


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('cart', 'product', 'quantity',
                  'price', 'total_price', 'status')


class WishlistSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        return GetWishlistItemSerializer(obj.items.all(), many=True).data

    class Meta:
        model = Wishlist
        fields = ('key', 'created_at', 'updated_at', 'customer', 'status', 'items')
        read_only_fields = ('key', 'created_at', 'items')


class GetWishlistItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, obj):
        return {
            'name': obj.product.name,
            'slug': obj.product.slug,
            'selling_price': obj.product.selling_price,
            'images': obj.product.images.url if obj.product.images else ''
        }

    class Meta:
        model = WishlistItem
        fields = ('product',)
        read_only_fields = ('product',)


class StoreWishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ('wishlist', 'product')
