# Generated by Django 5.0.6 on 2024-08-10 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0004_alter_cashregister_name_alter_cashregister_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashregister',
            name='name',
            field=models.CharField(default='DESKTOP-0JB92VA', max_length=50),
        ),
        migrations.AlterField(
            model_name='cashregister',
            name='number',
            field=models.CharField(db_index=True, default='bb0ef6442a00', max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
