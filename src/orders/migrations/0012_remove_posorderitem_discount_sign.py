# Generated by Django 5.2 on 2025-05-03 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_posorderitem_is_active_posorderitem_is_enabled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posorderitem',
            name='discount_sign',
        ),
    ]
