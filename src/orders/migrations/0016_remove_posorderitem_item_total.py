# Generated by Django 5.2 on 2025-05-03 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_posorderitem_discounted_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posorderitem',
            name='item_total',
        ),
    ]
