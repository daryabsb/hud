# Generated by Django 5.2 on 2025-05-03 12:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0047_alter_document_date_alter_document_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 3, 15, 16, 56, 936295)),
        ),
        migrations.AlterField(
            model_name='document',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 18, 15, 16, 56, 936295)),
        ),
    ]
