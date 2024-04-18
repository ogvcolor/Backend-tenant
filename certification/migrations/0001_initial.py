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
            name='ChartProof',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('reference_name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rows', models.IntegerField(default=0)),
                ('columns', models.IntegerField(default=0)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CMYKDataSet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('reference_name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('illuminant', models.CharField(blank=True, null=True)),
                ('observer', models.CharField(blank=True, null=True)),
                ('filter', models.CharField(choices=[('M0', 'M0'), ('M1', 'M1'), ('M2', 'M2'), ('M3', 'M3')], default='M0', max_length=2)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ComparisonResults',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('paper', models.FloatField(max_length=20)),
                ('average', models.FloatField(max_length=20)),
                ('maximum', models.FloatField(max_length=20)),
                ('primary_maximum', models.FloatField(max_length=20)),
                ('CMYK', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(max_length=20), default=list, size=4)),
                ('secondary', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(max_length=20), default=list, size=3)),
                ('cmyk_dataset', models.ForeignKey(default='f6e6bbfe-60a7-4a4e-90a9-b75dbbc9a1ef', on_delete=django.db.models.deletion.DO_NOTHING, to='certification.cmykdataset')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CMYKData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('reference_name', models.CharField(max_length=100)),
                ('sample_id', models.CharField(max_length=100, null=True)),
                ('sample_name', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cmyk', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(max_length=20), default=list, size=4)),
                ('lab', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(max_length=20), default=list, null=True, size=3)),
                ('rgb', models.CharField(default='rgb(255, 255, 255)', null=True, verbose_name='RGB')),
                ('chart_proof', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cmyk_data', to='certification.chartproof')),
                ('cmyk_dataset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cmyk_data', to='certification.cmykdataset')),
                ('comparison_results', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cmyk_data', to='certification.comparisonresults')),
            ],
        ),
        migrations.CreateModel(
            name='Tolerance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('paper', models.JSONField(max_length=20)),
                ('average', models.JSONField(max_length=20)),
                ('maximum', models.JSONField(max_length=20)),
                ('primary_maximum', models.JSONField(max_length=20)),
                ('CMYK', models.JSONField(max_length=20)),
                ('secondary', models.JSONField(max_length=20)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comparisonresults',
            name='tolerance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='certification.tolerance'),
        ),
    ]