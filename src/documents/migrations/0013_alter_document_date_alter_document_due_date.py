# Generated by Django 5.0.6 on 2024-12-06 09:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0012_alter_document_date_alter_document_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 6, 12, 41, 51, 776933)),
        ),
        migrations.AlterField(
            model_name='document',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 21, 12, 41, 51, 776933)),
        ),
    ]
