# Generated by Django 5.0.6 on 2024-12-13 08:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0015_alter_document_date_alter_document_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 13, 11, 59, 9, 419939)),
        ),
        migrations.AlterField(
            model_name='document',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 28, 11, 59, 9, 419939)),
        ),
    ]
