from django.contrib.auth.models import AbstractUser
from django.db import models
from backend.enums.gender import Gender

from backend.enums.user import User as UserEnum


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [(u.value, u) for u in UserEnum]
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=UserEnum.STAFF.value)


class Customer(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='customer',
        related_query_name='customer',
        choices=[
            (u.id, u.username) for u in
            CustomUser.objects.filter(user_type=UserEnum.CUSTOMER.value)
        ]
    )
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=1, null=True, blank=True, choices=[(g.value, g.value) for g in Gender])
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_user(self):
        return self.user

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.user:
            user = CustomUser.objects.create_user(
                username=self.phone,
                password='123456',
                first_name=self.name,
                user_type=UserEnum.CUSTOMER.value)
            self.user = user
        else:
            self.user.first_name = self.name
            
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
