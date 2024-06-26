# Generated by Django 5.0.6 on 2024-05-22 14:53

import django.db.models.deletion
import src.core.modules
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customer_customerdiscount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('number', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(default='Zeneon Company Logo', max_length=100)),
                ('image', models.ImageField(blank=True, default='uploads/logo/7a81a70d-3fe0-4c24-ba80-d1bf7f95b5a0.png', null=True, upload_to=src.core.modules.upload_image_file_path)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('number', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('tax_number', models.CharField(default='N/A', max_length=200)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('postal_code', models.CharField(default='00000', max_length=20)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(default='Iraq', max_length=50)),
                ('street', models.CharField(blank=True, max_length=350, null=True)),
                ('name', models.CharField(max_length=200)),
                ('handle', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('is_default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='companies', to=settings.AUTH_USER_MODEL)),
                ('logo', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company', to='accounts.logo')),
            ],
            options={
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('number', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('tax_number', models.CharField(default='N/A', max_length=200)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('postal_code', models.CharField(default='00000', max_length=20)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(default='Iraq', max_length=50)),
                ('street', models.CharField(blank=True, max_length=350, null=True)),
                ('name', models.CharField(max_length=200)),
                ('handle', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('is_default', models.BooleanField(default=False)),
                ('hashed_license', models.CharField(blank=True, max_length=100, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='accounts.company')),
                ('logo', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='store', to='accounts.logo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'stores',
            },
        ),
    ]
