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
    class Meta:
        model = Wishlist
        fields = ('key', 'created_at', 'updated_at', 'customer', 'status')
        read_only_fields = ('key', 'created_at')


class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ('wishlist', 'product', 'status', 'created_at', 'updated_at')
