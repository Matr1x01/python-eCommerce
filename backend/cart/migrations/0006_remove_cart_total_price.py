# Generated by Django 5.0.6 on 2024-06-06 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_remove_cartitem_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total_price',
        ),
    ]