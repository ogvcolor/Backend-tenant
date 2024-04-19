# Generated by Django 5.0.1 on 2024-04-19 18:09

import django.db.models.deletion
import login.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AccessLevel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('profile', models.CharField(max_length=100)),
                ('column', models.CharField(max_length=100)),
                ('title', models.CharField(default='Plant', max_length=100)),
                ('source_column', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccessLevel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('auth_user', models.CharField(max_length=100)),
                ('user_email', models.CharField(max_length=100)),
                ('access_level', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('job_position', models.CharField(max_length=100)),
                ('directory', models.CharField(max_length=100)),
                ('email', models.CharField(default='teste@teste.com.br', max_length=200)),
                ('privacy_policy', models.BooleanField(default=False)),
                ('canseename', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=login.models.get_current_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
