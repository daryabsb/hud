# Generated by Django 5.0.6 on 2024-11-25 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_posorder_document_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posorder',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
