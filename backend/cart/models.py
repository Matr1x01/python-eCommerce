from django.db import models
from users.models import Customer
from address.models import Address
from product.models import Product
from backend.enums.status import Status
import uuid
from backend.enums.DeliveryMethod import DeliveryMethod

from coupons.models import Coupon


class ActiveCartItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Status.ACTIVE.value)


class ActiveWishlistItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Status.ACTIVE.value)


class Wishlist(models.Model):
    key = models.UUIDField(unique=True, editable=False,
                           null=False, blank=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.OneToOneField(
        Customer, related_name='wishlist', on_delete=models.CASCADE, null=False, blank=False)
    status = models.SmallIntegerField(
        choices=[(s.value, s.name) for s in Status], default=Status.ACTIVE.value)

    def __str__(self):
        return self.customer.user.customer.name + "-" + str(self.key)


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist, related_name='items', on_delete=models.CASCADE, null=False, blank=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, blank=False, related_name='wishlist_items')
    status = models.SmallIntegerField(
        choices=[(s.value, s.name) for s in Status], default=Status.ACTIVE.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ActiveWishlistItemManager()

    def __str__(self):
        return self.product.name + "-" + str(self.wishlist.key)


class Cart(models.Model):
    key = models.UUIDField(unique=True, editable=False,
                           null=False, blank=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(
        Customer, related_name='cart', on_delete=models.CASCADE, null=False, blank=False)
    subtotal_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    total_items = models.IntegerField(default=0)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_method = models.CharField(max_length=255, null=False, blank=False, default=DeliveryMethod.HOME_DELIVERY.value)
    address = models.ForeignKey(Address, related_name='cart', null=False, blank=False, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, related_name='carts', null=True, blank=True, on_delete=models.DO_NOTHING)
    status = models.SmallIntegerField(
        choices=[(s.value, s.name) for s in Status], default=Status.ACTIVE.value)
    
    def __str__(self):
        return self.customer.user.customer.name + "-" + str(self.key)

    class Meta:
        db_table = 'cart'
        ordering = ['-created_at']


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, related_name='items', on_delete=models.CASCADE, null=False, blank=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, blank=False, related_name='cart_items')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00) 
    status = models.SmallIntegerField(
        choices=[(s.value, s.name) for s in Status], default=Status.ACTIVE.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ActiveCartItemManager()

    def __str__(self):
        return self.product.name + "-" + str(self.cart.key)

    class Meta:
        db_table = 'cart_item'
        ordering = ['-created_at']
