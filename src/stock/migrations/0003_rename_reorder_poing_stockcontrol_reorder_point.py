# Generated by Django 5.0.6 on 2024-05-25 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_alter_stock_warehouse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockcontrol',
            old_name='reorder_poing',
            new_name='reorder_point',
        ),
    ]
