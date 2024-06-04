from django.db import models
from users.models import Customer
from address.models import Address
from product.models import Product
from backend.enums.status import Status


class Wishlist(models.Model):
    key = models.UUIDField(unique=True, editable=False,
                           null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.OneToOneField(
        Customer, related_name='wishlist', on_delete=models.CASCADE, null=False, blank=False)
    status = models.SmallIntegerField(
        choices=[(s.value, s.name) for s in Status], default=Status.ACTIVE.value)


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist, related_name='items', on_delete=models.CASCADE, null=False, blank=False)
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, null=False, blank=False, related_name='wishlist_items')
    status = models.SmallIntegerField(
        choices=[(s.value, s.name) for s in Status], default=Status.ACTIVE.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    key = models.UUIDField(unique=True, editable=False,
                           null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.OneToOneField(
        Customer, related_name='cart', on_delete=models.CASCADE, null=False, blank=False)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    subtotal_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    total_items = models.IntegerField(default=0)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.OneToOneField(
        Address, related_name='cart', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.SmallIntegerField(
        choices=[(s.value, s.name) for s in Status], default=Status.ACTIVE.value)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, related_name='items', on_delete=models.CASCADE, null=False, blank=False)
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, null=False, blank=False, related_name='cart_items')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    status = models.SmallIntegerField(
        choices=[(s.value, s.name) for s in Status], default=Status.ACTIVE.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
