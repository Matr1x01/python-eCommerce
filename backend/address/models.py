from django.db import models
import uuid
from users.models import Customer


class Address(models.Model):
    address = models.TextField()
    uuid = models.UUIDField(unique=True, editable=False, null=False, blank=False, default=uuid.uuid4)
    area = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    customer = models.ForeignKey(
        Customer,
        related_name='addresses',
        on_delete=models.DO_NOTHING,
        null=False, blank=False)

    def __str__(self):
        return self.address

    class Meta:
        db_table = 'addresses'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class DeliveryCharge(models.Model):
    postal_code = models.CharField(max_length=255)
    charge = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.postal_code

    class Meta:
        db_table = 'delivery_charges'
        verbose_name = 'Delivery Charge'
        verbose_name_plural = 'Delivery Charges'
