from django.db import models
from order.models import Order
from backend.enums.status import Status


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=50)
    status = models.SmallIntegerField(choices=[(s.value, s.name) for s in Status], default=Status.ACTIVE.value)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.order} {self.amount}'