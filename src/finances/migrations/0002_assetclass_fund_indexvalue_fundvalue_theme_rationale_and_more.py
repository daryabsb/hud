# Generated by Django 5.0.6 on 2024-07-12 11:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_region'),
        ('finances', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Asset Classes',
            },
        ),
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('market_summary', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='IndexValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FundValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('value', models.IntegerField()),
                ('fund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.fund')),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('target_PL', models.IntegerField()),
                ('live', models.BooleanField()),
                ('asset_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.assetclass')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.country')),
                ('fund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.fund')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.region')),
            ],
        ),
        migrations.CreateModel(
            name='Rationale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=10)),
                ('rationale', models.TextField()),
                ('date', models.DateField()),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.theme')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('var', models.IntegerField()),
                ('cvar', models.IntegerField()),
                ('LTD', models.IntegerField()),
                ('SL', models.IntegerField()),
                ('theme', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='finances.theme')),
            ],
        ),
    ]