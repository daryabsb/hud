# Generated by Django 5.0.6 on 2024-06-01 16:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurations', '0002_applicationproperty_applicationpropertysection'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationproperty',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='application_properties', to='configurations.applicationpropertysection'),
        ),
    ]
