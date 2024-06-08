# Generated by Django 5.0.6 on 2024-06-08 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.SmallIntegerField(choices=[(1, 'PENDING'), (2, 'CONFIRMED'), (3, 'CANCELLED'), (4, 'DELIVERED')], default=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.SmallIntegerField(choices=[(1, 'UNPAID'), (2, 'PAID'), (3, 'REFUNDED'), (4, 'PARTIALLY_REFUNDED'), (5, 'PAYMENT_FAILED'), (6, 'CANCELLED')], default=1),
        ),
    ]
