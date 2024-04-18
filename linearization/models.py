from django.db import models
from django.contrib.postgres.fields import ArrayField
from login.models import CustomUser
import uuid
from datetime import datetime

# Mapeamento dos process curve sets aos nominais e targets correspondentes
DEFAULT_PROCESS_CURVE_SET = 'ISO 12647-2 Curve A'
PROCESS_CURVE_SETS = {
    DEFAULT_PROCESS_CURVE_SET: {'nominal': [0.0, 5.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 95.0, 100.0], 'target': [0.0, 7.0, 14.0, 27.6, 40.7, 53.0, 64.3, 74.5, 83.4, 90.7, 96.3, 98.4, 100.0]},
    'ISO 12647-2 Curve B': {'nominal': [0.0, 5.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 95.0, 100.0], 'target': [0.0, 8.0, 15.6, 30.2, 43.7, 56.0, 67.0, 76.6, 84.9, 91.5, 96.6, 98.5, 100.0]},
    'ISO 12647-2 Curve C': {'nominal': [0.0, 5.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 95.0, 100.0], 'target': [0.0, 8.9, 17.3, 32.8, 46.7, 59.0, 69.6, 78.7, 86.3, 92.3, 96.9, 98.6, 100.0]},
    'ISO 12647-2 Curve D': {'nominal': [0.0, 5.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 95.0, 100.0], 'target': [0.0, 9.8, 18.9, 35.5, 49.8, 62.0, 72.3, 80.8, 87.6, 93.0, 97.1, 98.7, 100.0]},
    'ISO 12647-2 Curve E': {'nominal': [0.0, 3.0, 5.0, 10.0, 15.0, 20.0, 25.0, 29.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 61.0, 65.0, 70.0, 80.0, 90.0, 95.0, 97.0, 100.0], 'target': [0.0, 7.18, 11.8, 22.6, 32.37, 41.2, 49.23, 55.03, 56.4, 62.82, 68.5, 73.55, 78.0, 81.9, 85.3, 85.9, 88.2, 90.7, 94.7, 97.7, 98.9, 99.35, 100.0]},
    'ISO 12647-2 Curve F': {'nominal': [0.0, 5.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 95.0, 100.0], 'target': [0.0, 11.7, 22.3, 40.8, 55.9, 68.0, 77.5, 84.8, 90.3, 94.4, 97.5, 98.8, 100.0]},
    'ISO 12647-2 Curve A(70)': {'nominal': [0.0, 5.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 95.0, 100.0], 'target': [0.0, 7.3, 14.6, 28.5, 41.7, 54.0, 65.2, 75.2, 83.9, 91.0, 96.4, 98.5, 100.0]},
    'ISO 12647-2 Curve B(70)': {'nominal': [0.0, 5.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 95.0, 100.0], 'target': [0.0, 8.6, 16.7, 32.0, 45.7, 58.0, 68.8, 78.0, 85.8, 92.1, 96.8, 98.6, 100.0]},
}

class TargetSet(models.Model):
    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, primary_key=True)
    name = models.CharField('Target Set Name', max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # user_id pode ser blank para os ProcessCurveSet pre-definidos
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

class CalibrationProject(models.Model):
    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    calibration_project = models.CharField('Project Name', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

COLOR = [
    ('C', 'Cyan'), ('M', 'Magenta'), ('Y', 'Yellow'), ('K', 'Black'), ('OTHER', 'Other Colors')
]

class ColorSet(models.Model):
    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    color = ArrayField(models.CharField(max_length=20)) 
    target_set = models.ForeignKey(TargetSet, on_delete=models.CASCADE, null=True)
    nominal = ArrayField(models.FloatField(max_length=20))
    target = ArrayField(models.FloatField(max_length=20))
    comment = models.CharField(max_length=200, blank=True, default="")

class MeasuredValues(models.Model):
    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, primary_key=True)
    color_info = models.ForeignKey(ColorSet, on_delete=models.CASCADE)
    target_set = models.ForeignKey(TargetSet, on_delete=models.CASCADE, null=True)
    measured = ArrayField(models.FloatField(max_length=20))
    calibration_project = models.ForeignKey(CalibrationProject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)