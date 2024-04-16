# Generated by Django 5.0.1 on 2024-04-11 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLevel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
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
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('auth_user', models.CharField(max_length=100)),
                ('user_email', models.CharField(max_length=100)),
                ('access_level', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('job_position', models.CharField(max_length=100)),
                ('directory', models.CharField(max_length=100)),
                ('email', models.CharField(default='teste@teste.com.br', max_length=200)),
                ('privacy_policy', models.BooleanField(default=False)),
                ('canseename', models.BooleanField(default=False)),
            ],
        ),
    ]
