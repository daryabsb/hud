# Generated by Django 5.2 on 2025-04-30 09:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0028_alter_document_date_alter_document_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2025, 4, 30, 12, 5, 46, 965143)),
        ),
        migrations.AlterField(
            model_name='document',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 15, 12, 5, 46, 965143)),
        ),
    ]
