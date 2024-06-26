# Generated by Django 5.0.6 on 2024-06-29 19:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printers', '0002_printstation_posprinterselectionsettings_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='printstation',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='printstation',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
