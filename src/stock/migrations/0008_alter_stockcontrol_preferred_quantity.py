# Generated by Django 5.2 on 2025-04-22 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0007_alter_stock_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockcontrol',
            name='preferred_quantity',
            field=models.SmallIntegerField(default=1),
        ),
    ]
