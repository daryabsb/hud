# Generated by Django 5.0.6 on 2024-06-02 08:04

import django.db.models.deletion
import fontawesome_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurations', '0004_alter_applicationpropertysection_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationpropertysection',
            name='icon',
            field=fontawesome_5.fields.IconField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='applicationpropertysection',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='configurations.applicationpropertysection'),
        ),
    ]
