# Generated by Django 5.0.6 on 2024-06-01 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurations', '0003_applicationproperty_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationpropertysection',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]