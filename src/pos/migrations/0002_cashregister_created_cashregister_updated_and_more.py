# Generated by Django 5.0.6 on 2024-07-23 18:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashregister',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cashregister',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='cashregister',
            name='name',
            field=models.CharField(default='DARYA-HOME-DELL', max_length=50),
        ),
        migrations.AlterField(
            model_name='cashregister',
            name='number',
            field=models.CharField(db_index=True, default='509a4c12a32c', max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
