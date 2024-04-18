# Generated by Django 5.0.1 on 2024-04-18 17:21

import django.contrib.postgres.fields
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('creationDate', models.DateField(auto_now_add=True, verbose_name='Creation Date')),
                ('updateDate', models.DateField(auto_now=True, verbose_name='Update Date')),
                ('sampleName', models.CharField(max_length=100, verbose_name='Sample Name')),
                ('sampleId', models.IntegerField(verbose_name='Sample Id')),
                ('isGlobal', models.BooleanField(default=True)),
                ('type', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('Lab', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(max_length=20), default=list, size=3)),
                ('onlyLab', models.BooleanField(default=False)),
                ('rgb', models.CharField(default='rgb(255, 255, 255)', null=True, verbose_name='RGB')),
                ('userId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SpectralNumber',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Creation Date')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='Update Date')),
                ('spectralNumber', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(max_length=20), default=list, size=36)),
                ('filter', models.CharField(choices=[('M0', 'M0'), ('M1', 'M1'), ('M2', 'M2'), ('M3', 'M3')], default='M0', max_length=2)),
                ('colorId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='spectral_numbers', to='color.color')),
                ('userId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]