# Generated by Django 5.0.6 on 2024-05-23 15:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='currency',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.currency'),
        ),
    ]