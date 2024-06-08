import uuid
from django.db import models

from backend.enums.status import Status
from product.models import Product
from users.models import Customer
from address.models import Address
from backend.enums.OrderStatus import OrderStatus
from backend.enums.PaymentStatus import PaymentStatus


class Order(models.Model):
    key = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    total_items = models.IntegerField(default=0)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.SmallIntegerField(
        choices=[(status.value, status.name) for status in OrderStatus], default=OrderStatus.PENDING.value)
    payment_method = models.CharField(max_length=50)
    payment_status = models.SmallIntegerField(
        choices=[(status.value, status.name) for status in PaymentStatus], default=PaymentStatus.UNPAID.value)
    shipping_address = models.CharField(max_length=255)
    status = models.SmallIntegerField(
        choices=[(s.value, s.name) for s in Status], default=Status.ACTIVE.value)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.customer.name+" "+self.key


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=False, blank=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.SmallIntegerField(
        choices=[(s.value, s.name) for s in Status], default=Status.ACTIVE.value)

    def __str__(self):
        return self.product.name+" "+self.order.key
