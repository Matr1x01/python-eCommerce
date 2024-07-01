from datetime import datetime
from django.db import transaction
from urllib.parse import urljoin
from rest_framework import serializers
from django.conf import settings
from backend.enums.OrderStatus import OrderStatus
from backend.enums.PaymentStatus import PaymentStatus
from backend.enums.DeliveryMethod import DeliveryMethod
from backend.enums.PaymentMethod import PaymentMethod
from backend.enums.status import Status

from order.models import Order

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), write_only=True)
    payment_method = serializers.CharField(
        max_length=255, required=True, write_only=True)
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=True, write_only=True)
    transaction_id = serializers.CharField(
        max_length=255, required=False, write_only=True)
    payment_status = serializers.SerializerMethodField()
    payment_method_name = serializers.SerializerMethodField()
    order_key = serializers.SerializerMethodField()
    order_status = serializers.SerializerMethodField()
    order_total = serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()

    def get_payment_status(self, obj):
        return PaymentStatus(obj.payment_status).name

    def get_payment_method_name(self, obj):
        return PaymentMethod(obj.payment_method).name

    def get_order_key(self, obj):
        return obj.order.key

    def get_order_status(self, obj):
        return OrderStatus(obj.order.order_status).name

    def get_order_total(self, obj):
        return obj.order.total

    def get_order_date(self, obj):
        return obj.order.date

    class Meta:
        model = Payment
        fields = (
            'order', 'amount', 'transaction_id', 'payment_method', 'payment_status', 'payment_method_name', 'order_key',
            'order_status', 'order_total', 'order_date',)
        read_only_fields = ('payment_status', 'payment_method_name', 'order_key', 'order_status', 'order_total',
                            'order_date',)

    def validate_payment_method(self, value):
        try:
            return PaymentMethod(value).value
        except ValueError:
            raise serializers.ValidationError('Invalid payment method')

    def create(self, data):
        order = data.get('order')
        if order.payment_status == PaymentStatus.PAID.value:
            raise serializers.ValidationError('Order has already been paid')
        with transaction.atomic():
            try:
                payment = Payment.objects.create(
                    order=order,
                    amount=self.validated_data['amount'],
                    transaction_id=self.validated_data.get('transaction_id'),
                    payment_method=self.validated_data['payment_method'],
                    date=datetime.now()
                )
            except Exception as e:
                raise serializers.ValidationError(e)

            order.payment_status = PaymentStatus.PAID.value
            order.save()

            return payment

    def validate(self, attrs):
        if attrs.get('transaction_id') and not attrs.get('payment_method'):
            raise serializers.ValidationError('Payment method is required when transaction ID is provided')

        return attrs
