# Generated by Django 5.0.6 on 2024-05-22 09:20

import django.db.models.deletion
import django.db.models.expressions
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_customer_customerdiscount_and_more'),
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PosOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_subtotal', models.DecimalField(decimal_places=3, default=0, max_digits=15)),
                ('discount', models.FloatField(default=0)),
                ('discount_type', models.FloatField(default=0)),
                ('discounted_amount', models.GeneratedField(db_persist=True, expression=models.Case(models.When(discount_type=1, then=django.db.models.expressions.CombinedExpression(models.F('item_subtotal'), '*', django.db.models.expressions.CombinedExpression(models.F('discount'), '/', models.Value(100)))), models.When(discount_type=0, then=models.F('discount')), default=models.Value(0), output_field=models.DecimalField(decimal_places=3, default=0, max_digits=15)), output_field=models.DecimalField(decimal_places=3, default=0, max_digits=15))),
                ('discount_sign', models.GeneratedField(db_persist=False, expression=models.Case(models.When(discount_type=1, then=models.Value('%')), models.When(discount_type=0, then=models.Value('$')), default=models.Value(''), output_field=models.CharField(max_length=20)), output_field=models.CharField(max_length=20))),
                ('subtotal_after_discount', models.GeneratedField(db_persist=False, expression=django.db.models.expressions.CombinedExpression(models.F('item_subtotal'), '-', models.F('discounted_amount')), output_field=models.DecimalField(decimal_places=3, default=0, max_digits=15))),
                ('fixed_taxes', models.DecimalField(decimal_places=3, default=0, max_digits=15)),
                ('total_tax_rate', models.DecimalField(decimal_places=3, default=0, max_digits=15)),
                ('total_tax', models.GeneratedField(db_persist=False, expression=django.db.models.expressions.CombinedExpression(models.F('fixed_taxes'), '+', django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('subtotal_after_discount'), '*', models.F('total_tax_rate')), '/', models.Value(100))), output_field=models.DecimalField(decimal_places=3, default=0, max_digits=15))),
                ('total', models.GeneratedField(db_persist=False, expression=django.db.models.expressions.CombinedExpression(models.F('subtotal_after_discount'), '+', models.F('total_tax')), output_field=models.DecimalField(decimal_places=3, default=0, max_digits=15))),
                ('status', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='accounts.customer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='PosOrderItem',
            fields=[
                ('number', models.CharField(db_index=True, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('round_number', models.DecimalField(decimal_places=3, default=0, max_digits=4)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=3, default=0, max_digits=15)),
                ('is_locked', models.BooleanField(default=False)),
                ('discount', models.FloatField(default=0)),
                ('discount_type', models.FloatField(default=0)),
                ('discounted_amount', models.GeneratedField(db_persist=True, expression=models.Case(models.When(discount_type=1, then=django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('price'), '*', models.F('quantity')), '*', django.db.models.expressions.CombinedExpression(models.F('discount'), '/', models.Value(100)))), models.When(discount_type=0, then=models.F('discount')), default=models.Value(0), output_field=models.DecimalField(decimal_places=3, default=0, max_digits=15)), output_field=models.DecimalField(decimal_places=3, default=0, max_digits=15))),
                ('discount_sign', models.GeneratedField(db_persist=False, expression=models.Case(models.When(discount_type=1, then=models.Value('%')), models.When(discount_type=0, then=models.Value('$')), default=models.Value(''), output_field=models.CharField(max_length=20)), output_field=models.CharField(max_length=20))),
                ('item_total', models.GeneratedField(db_persist=True, expression=models.Case(models.When(discount_type=1, then=django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('price'), '*', models.F('quantity')), '-', django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('price'), '*', models.F('quantity')), '*', django.db.models.expressions.CombinedExpression(models.F('discount'), '/', models.Value(100))))), models.When(discount_type=0, then=django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('price'), '*', models.F('quantity')), '-', models.F('discount'))), default=models.Value(0), output_field=models.DecimalField(decimal_places=3, default=0, max_digits=15)), output_field=models.DecimalField(decimal_places=3, default=0, max_digits=15))),
                ('is_featured', models.BooleanField(default=False)),
                ('voided_by', models.SmallIntegerField(default=0)),
                ('comment', models.TextField(blank=True, null=True)),
                ('bundle', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.posorder')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_items', to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]