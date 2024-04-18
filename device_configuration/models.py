from django.db import models
from login.models import CustomUser
import uuid

# Create your models here.
"""
    Device Preferences
"""

class Device_information(models.Model):
    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, primary_key=True)
    user_id =  models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    creation_date = models.DateField('Creation Date', auto_now_add=True)
    current_device = models.BooleanField('Current Device', default=False)
    device_name = models.CharField('Device Name', max_length=100)
    device_serial = models.CharField('Device Serial', max_length=100)
    measurement_mode = models.CharField('Measurement Mode', max_length=100)