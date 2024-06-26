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

    class Meta:
        db_table = 'coupons'
        ordering = ('-created_at',)


class CouponHistory(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='history')
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, related_name='coupons')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.coupon.code} {self.order.key}'

    class Meta:
        db_table = 'coupon_history'
        ordering = ('-created_at',)
