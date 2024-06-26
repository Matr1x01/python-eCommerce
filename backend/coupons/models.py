from django.db import models
from backend.enums.status import Status

class Coupon(models.Model):
    code = models.CharField(max_length=255, unique=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.SmallIntegerField(choices=[(s.value, s.name) for s in Status], default=Status.ACTIVE.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
