# Generated by Django 5.0.6 on 2024-12-13 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_company_ar_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pin',
            field=models.SmallIntegerField(default=1699),
        ),
    ]
