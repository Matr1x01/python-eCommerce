# Generated by Django 5.0.6 on 2024-06-03 10:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_customer_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('user', models.OneToOneField(blank=True, choices=[(1, 'matrix')], null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff', related_query_name='staff', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
