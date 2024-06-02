# Generated by Django 5.0.6 on 2024-06-02 12:09

import backend.enums.user
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(0, backend.enums.user.User['ADMIN']), (1, backend.enums.user.User['STAFF']), (2, backend.enums.user.User['CUSTOMER'])], default=1),
        ),
    ]