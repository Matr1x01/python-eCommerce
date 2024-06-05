from backend.enums.status import Status
from product.models import Product
from .models import Cart, CartItem, Wishlist, WishlistItem
from rest_framework import serializers


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('key', 'created_at', 'updated_at', 'customer', 'total_price', 'subtotal_price',
                  'total_items', 'discount', 'tax', 'shipping', 'total', 'address', 'status')
        read_only_fields = ('key', 'created_at')

    def create(self, validated_data):
        try:
            cart = Cart.objects.create(**validated_data)
            return cart
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(required=True)

    class Meta:
        model = CartItem
        fields = ('cart', 'product', 'quantity', 'status')
        read_only_fields = ('cart', 'status')


class GetCartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, obj):
        return {
            'name': obj.product.name,
            'slug': obj.product.slug,
            'selling_price': obj.product.selling_price,
            'images': obj.product.images.url if obj.product.images else ''
        }

    class Meta:
        model = CartItem
        fields = ('product', 'quantity')
        read_only_fields = ('product', 'quantity')

        



class WishlistSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        return GetWishlistItemSerializer(obj.items.filter(status=Status.ACTIVE.value).all(), many=True).data

    class Meta:
        model = Wishlist
        fields = ('key', 'created_at', 'updated_at', 'status', 'items')
        read_only_fields = ('key', 'created_at', 'items')

    def create(self, validated_data):
        try:
            wishlist = Wishlist.objects.create(**validated_data)
            return wishlist
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

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


class WishlistItemSerializer(serializers.ModelSerializer):

    product = serializers.CharField(required=True)
    class Meta:
        model = WishlistItem
        fields = ('product',)
        read_only_fields = ('product',)