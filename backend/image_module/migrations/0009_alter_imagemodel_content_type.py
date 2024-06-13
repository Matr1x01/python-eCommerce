# Generated by Django 5.0.6 on 2024-06-13 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('image_module', '0008_alter_imagemodel_content_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_collection', to='contenttypes.contenttype'),
        ),
    ]
