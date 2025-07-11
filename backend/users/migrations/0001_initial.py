# Generated by Django 5.2.3 on 2025-06-27 21:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('employee_id', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('department', models.CharField(choices=[('KITCHEN', 'Kitchen'), ('MANAGEMENT', 'Management'), ('ACCOUNTS', 'Accounts'), ('SUPERVISOR', 'Supervisor'), ('OTHER', 'Other')], default='OTHER', max_length=20)),
                ('position', models.CharField(blank=True, max_length=100, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/admins/')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Admin Profile',
                'verbose_name_plural': 'Admin Profiles',
            },
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('roll_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/customers/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer Profile',
                'verbose_name_plural': 'Customer Profiles',
            },
        ),
    ]
