# Generated by Django 5.0.6 on 2024-08-09 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurations', '0013_alter_apptablecolumn_related_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='apptablecolumn',
            name='orderable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='apptablecolumn',
            name='searchable',
            field=models.BooleanField(default=False),
        ),
    ]