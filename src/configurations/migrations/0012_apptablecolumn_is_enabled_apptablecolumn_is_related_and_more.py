# Generated by Django 5.0.6 on 2024-08-02 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurations', '0011_apptable_apptablecolumn'),
    ]

    operations = [
        migrations.AddField(
            model_name='apptablecolumn',
            name='is_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='apptablecolumn',
            name='is_related',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='apptablecolumn',
            name='related_value',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
