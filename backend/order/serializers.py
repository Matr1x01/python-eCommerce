from datetime import datetime
from django.db import transaction
from urllib.parse import urljoin
from rest_framework import serializers
from django.conf import settings
from order.models import Order, OrderItem
from cart.models import Cart
from backend.enums.OrderStatus import OrderStatus
from backend.enums.PaymentStatus import PaymentStatus
from backend.enums.DeliveryMethod import DeliveryMethod
from backend.enums.PaymentMethod import PaymentMethod
from backend.enums.status import Status
from coupons.models import CouponHistory


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_slug = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_slug(self, obj):
        return obj.product.slug

    def get_product_image(self, obj):
        return [urljoin(settings.APP_URL, image.image.url) for image in obj.product.images]

    class Meta:
        model = OrderItem
        fields = ('quantity', 'price', 'total', 'product_name',
                  'product_slug', 'product_image')
        read_only_fields = fields


class OrderDetailsSerializer(serializers.ModelSerializer):
    order_status = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    payment_method = serializers.SerializerMethodField()
    delivery_method = serializers.SerializerMethodField()
    ordered_items = OrderItemSerializer(source='items', many=True)
    address = serializers.SerializerMethodField()

    def get_order_status(self, obj):
        return OrderStatus(obj.order_status).name

    def get_payment_status(self, obj):
        return PaymentStatus(obj.payment_status).name

    def get_payment_method(self, obj):
        return PaymentMethod(obj.payment_method).name

    def get_delivery_method(self, obj):
        return DeliveryMethod(obj.delivery_method).name

    def get_address(self, obj):
        return str(obj.address)

    class Meta:
        model = Order
        fields = ('key', 'total', 'tax', 'shipping', 'discount', 'sub_total', 'total_items', 'date', 'order_status',
                  'payment_status', 'payment_method', 'delivery_method', 'ordered_items', 'address')
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    payment_method = serializers.CharField(
        max_length=255, required=True, write_only=True)
    delivery_method = serializers.CharField(
        max_length=255, required=True, write_only=True)
    cart = serializers.PrimaryKeyRelatedField(
        queryset=Cart.objects.all(), write_only=True)
    order_status = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    payment_method_name = serializers.SerializerMethodField()
    delivery_method_name = serializers.SerializerMethodField()

    def get_order_status(self, obj):
        return OrderStatus(obj.order_status).name

    def get_payment_status(self, obj):
        return PaymentStatus(obj.payment_status).name

    def get_payment_method_name(self, obj):
        return PaymentMethod(obj.payment_method).name

    def get_delivery_method_name(self, obj):
        return DeliveryMethod(obj.delivery_method).name

    class Meta:
        model = Order
        fields = ('key', 'total', 'total_items', 'date', 'order_status', 'payment_status', 'payment_method', 'delivery_method', 'cart',
                  'payment_method_name', 'delivery_method_name')
        read_only_fields = ('key', 'total', 'date', 'order_status',
                            'payment_status', 'payment_method_name', 'delivery_method_name')

    def validate(self, data):
        cart = data.get('cart')
        if not cart.items.exists():
            raise serializers.ValidationError('Cart is empty')
        return data

    def validate_delivery_method(self, value):
        try:
            return DeliveryMethod(value).value
        except ValueError:
            raise serializers.ValidationError('Invalid delivery method')

    def validate_payment_method(self, value):
        try:
            return PaymentMethod(value).value
        except ValueError:
            raise serializers.ValidationError('Invalid payment method')

    def create(self, data):
        cart = data.get('cart')
        if len(cart.items.all()) == 0:
            raise serializers.ValidationError('Cart is empty')
        with transaction.atomic():
            try:
                order = Order.objects.create(
                    customer=cart.customer,
                    payment_method=self.validated_data['payment_method'],
                    delivery_method=self.validated_data['delivery_method'],
                    date=datetime.now(),
                    total_items=cart.total_items,
                    sub_total=cart.subtotal_price,
                    shipping=cart.shipping,
                    discount=cart.discount,
                    tax=cart.tax,
                    total=cart.total,
                    address=cart.address,
                )
                cart.status = Status.INACTIVE.value
                if cart.coupon:
                    CouponHistory.objects.create(
                        coupon=cart.coupon, order=order
                    )

                cart.save()
            except Exception as e:
                raise serializers.ValidationError(e)

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.price,
                    total=item.price * item.quantity
                )
                for item in cart.items.select_related('product').all()
            ]

            try:
                OrderItem.objects.bulk_create(order_items)
            except Exception as e:
                raise serializers.ValidationError(str(e))

            return order
