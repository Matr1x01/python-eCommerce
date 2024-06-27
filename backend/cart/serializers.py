from django.shortcuts import get_object_or_404
from backend.enums.status import Status
from product.models import Product
from .models import Cart, CartItem, Wishlist, WishlistItem
from urllib.parse import urljoin
from rest_framework import serializers
from django.conf import settings

from address.models import DeliveryCharge


class GetCartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_selling_price = serializers.DecimalField(
        source='product.get_price', max_digits=10, decimal_places=2, read_only=True)
    product_images = serializers.SerializerMethodField()
    quantity_in_cart = serializers.IntegerField(
        source='quantity', read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_product_images(self, obj):
        return [urljoin(settings.APP_URL, image.image.url) for image in obj.product.images]

    def get_total_price(self, obj):
        return obj.product.get_price() * obj.quantity

    class Meta:
        model = CartItem
        fields = ('product_name', 'product_slug', 'product_selling_price',
                  'product_images', 'quantity_in_cart', 'total_price')
        read_only_fields = fields


class CartSerializer(serializers.ModelSerializer):
    delivery_method = serializers.CharField(
        max_length=255, required=True, write_only=True)
    address = serializers.UUIDField(required=False, )
    total_items = serializers.IntegerField(read_only=True)
    subtotal_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    discount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    tax = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    shipping = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    total = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True)
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        return GetCartItemSerializer(obj.items.all(), many=True).data

    def calculate_cart_values(self, obj):
        delivery_charge = DeliveryCharge.objects.filter(postal_code=obj.address.postal_code).first()
        if delivery_charge:
            shipping = delivery_charge.charge
        else:
            shipping = 10

        subtotal_price = sum(item.product.get_price() *
                             item.quantity for item in obj.items.all())
        total_items = sum(item.quantity for item in obj.items.all())
        coupon = obj.coupon
        discount = obj.discount if obj.coupon else 0
        tax = 0
        total = subtotal_price - discount + tax + shipping

        if total_items == 0:
            total = 0
            discount = 0
            tax = 0
            shipping = 0
            coupon = None

        return {
            'subtotal_price': subtotal_price,
            'total_items': total_items,
            'discount': discount,
            'tax': tax,
            'shipping': shipping,
            'total': total,
            'coupon': coupon,
        }

    class Meta:
        model = Cart
        fields = ('key', 'subtotal_price', 'total_items',
                  'discount', 'tax', 'shipping', 'total', 'address', 'items', 'delivery_method')
        read_only_fields = fields

    def create(self, validated_data):
        try:
            cart = Cart.objects.create(**validated_data)
            return cart
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(), slug_field='slug', required=True)
    quantity = serializers.IntegerField(required=True)

    def validate(self, attrs):
        product = attrs.get('product')
        if isinstance(product, str):
            product = get_object_or_404(Product, slug=product)
        attrs['product'] = product
        attrs['price'] = product.get_price()
        return attrs

    class Meta:
        model = CartItem
        fields = ('product', 'quantity', 'price', 'status')
        read_only_fields = ('price', 'status')

    def create(self, data):
        try:
            data.price = data.product.get_price()
            return CartItem.objects.create(**data)
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})


class WishlistSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        return GetWishlistItemSerializer(obj.items.filter(status=Status.ACTIVE.value).all(), many=True).data

    class Meta:
        model = Wishlist
        fields = ('key',  'items',)
        read_only_fields = ('key', 'items')

    def create(self, validated_data):
        try:
            wishlist = Wishlist.objects.create(**validated_data)
            return wishlist
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})


class GetWishlistItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_selling_price = serializers.DecimalField(source='product.get_price', max_digits=10, decimal_places=2,
                                                     read_only=True)
    product_images = serializers.SerializerMethodField()

    def get_product_images(self, obj):
        return [urljoin(settings.APP_URL, image.image.url) for image in obj.product.images]

    class Meta:
        model = WishlistItem
        fields = ('product_name', 'product_slug', 'product_selling_price',
                  'product_images')  # Include 'product_images'
        read_only_fields = fields  # All fields are read-only


class WishlistItemSerializer(serializers.ModelSerializer):
    product = serializers.CharField(required=True)

    class Meta:
        model = WishlistItem
        fields = ('product',)
        read_only_fields = ('product',)


class CartAddressSerializer(serializers.Serializer):
    address = serializers.UUIDField(required=True)

    def validate(self, attrs):
        address = attrs.get('address')
        if not address:
            raise serializers.ValidationError('Address is required')

        address = self.context['request'].user.customer.addresses.filter(uuid=address).first()
        if not address:
            raise serializers.ValidationError('Valid Address is required')

        attrs['address'] = address

        return attrs
