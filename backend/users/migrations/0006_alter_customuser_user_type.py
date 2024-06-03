# Generated by Django 5.0.6 on 2024-06-03 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'ADMIN'), (1, 'STAFF'), (2, 'CUSTOMER')], default=1),
        ),
    ]
