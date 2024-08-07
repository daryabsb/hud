# Generated by Django 5.0.6 on 2024-07-14 10:06

import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printers', '0009_alter_companyletterhead_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyletterheadoption',
            name='bottom_margin',
            field=models.PositiveSmallIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='companyletterheadoption',
            name='left_margin',
            field=models.PositiveSmallIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='companyletterheadoption',
            name='paper_height',
            field=models.PositiveSmallIntegerField(default=297),
        ),
        migrations.AddField(
            model_name='companyletterheadoption',
            name='paper_width',
            field=models.PositiveSmallIntegerField(default=210),
        ),
        migrations.AddField(
            model_name='companyletterheadoption',
            name='paper_format',
            field=models.CharField(choices=[('A6', 'A4'), ('A5', 'A4'), ('A4', 'A4'), ('A3', 'A4'), ('A2', 'A4'), ('A1', 'A4')], default='A4', max_length=30),
        ),
        migrations.AddField(
            model_name='companyletterheadoption',
            name='right_margin',
            field=models.PositiveSmallIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='companyletterheadoption',
            name='top_margin',
            field=models.PositiveSmallIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='companyletterheadoption',
            name='inner_height',
            field=models.GeneratedField(db_persist=True, expression=django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('paper_height'), '-', models.F('left_margin')), '-', models.F('left_margin')), output_field=models.DecimalField(decimal_places=2, max_digits=5)),
        ),
        migrations.AddField(
            model_name='companyletterheadoption',
            name='inner_width',
            field=models.GeneratedField(db_persist=True, expression=django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('paper_width'), '-', models.F('left_margin')), '-', models.F('left_margin')), output_field=models.DecimalField(decimal_places=2, max_digits=5)),
        ),
    ]
