from backend.enums.status import Status
from product.models import Product
from .models import Cart, CartItem, Wishlist, WishlistItem
from rest_framework import serializers


class GetCartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_selling_price = serializers.DecimalField(source='product.selling_price', max_digits=10, decimal_places=2,
                                                     read_only=True)
    product_images = serializers.SerializerMethodField()
    quantity_in_cart = serializers.IntegerField(
        source='quantity', read_only=True) 

    def get_product_images(self, obj):
        return obj.product.images.url if obj.product.images else '' 

    class Meta:
        model = CartItem
        fields = ('product_name', 'product_slug', 'product_selling_price',
                  'product_images', 'quantity_in_cart', 'total_price')
        read_only_fields = fields


class CartSerializer(serializers.ModelSerializer):
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
        subtotal_price = 0
        total_items = 0
        discount = 0
        tax = 0
        shipping = 0
        total = 0
        for item in obj.items.all():
            subtotal_price += item.product.selling_price * item.quantity
            total_items += item.quantity
        total = subtotal_price - discount + tax + shipping
        return {
            'subtotal_price': subtotal_price,
            'total_items': total_items,
            'discount': discount,
            'tax': tax,
            'shipping': shipping,
            'total': total
        }

    class Meta:
        model = Cart
        fields = ('key', 'created_at', 'updated_at', 'subtotal_price',
                  'total_items', 'discount', 'tax', 'shipping', 'total', 'address', 'status', 'items',)
        read_only_fields = fields

    def create(self, validated_data):
        try:
            cart = Cart.objects.create(**validated_data)
            return cart
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

    def update(self, instance, validated_data):
        try:
            data = self.calculate_cart_values(instance)
            instance.subtotal_price = data['subtotal_price']
            instance.total_items = data['total_items']
            instance.discount = data['discount']
            instance.tax = data['tax']
            instance.shipping = data['shipping']
            instance.total = data['total']

            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(), slug_field='slug', required=True)
    quantity = serializers.IntegerField(required=True)

    def validate(self, attrs):
        product = attrs.get('product')
        if isinstance(product, str):
            product = Product.objects.filter(slug=product).first()
            if not product:
                raise serializers.ValidationError(
                    {"error": "Valid product is required"})

        attrs['product'] = product
        attrs['price'] = product.selling_price
        attrs['total_price'] = attrs['price'] * attrs['quantity']
        return attrs

    class Meta:
        model = CartItem
        fields = ('product', 'quantity', 'price', 'total_price', 'status')
        read_only_fields = ('price', 'total_price', 'status')

    def create(self, data):
        try:
            cart_item = CartItem.objects.create(**data)

            return cart_item
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})


class WishlistSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        return GetWishlistItemSerializer(obj.items.filter(status=Status.ACTIVE.value).all(), many=True).data

    class Meta:
        model = Wishlist
        fields = ('key', 'created_at', 'updated_at', 'status', 'items',)
        read_only_fields = ('key', 'created_at', 'items')

    def create(self, validated_data):
        try:
            wishlist = Wishlist.objects.create(**validated_data)
            return wishlist
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})


class GetWishlistItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_selling_price = serializers.DecimalField(source='product.selling_price', max_digits=10, decimal_places=2,
                                                     read_only=True)
    product_images = serializers.SerializerMethodField()

    def get_product_images(self, obj):
        return obj.product.images.url if obj.product.images else ''

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
