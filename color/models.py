"""Module providing a way to create a unique id"""

import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from login.models import CustomUser


class Color(models.Model):
    """Class representing color information"""

    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, primary_key=True)
    created_at = models.DateField("Creation Date", auto_now_add=True)
    updated_at = models.DateField("Update Date", auto_now=True)
    sample_name = models.CharField("Sample Name", max_length=100)
    sample_id = models.IntegerField("Sample Id")
    is_global = models.BooleanField(default=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=20)
    description = models.CharField(max_length=200, null=True, blank=True)
    lab = ArrayField(models.FloatField(max_length=20), size=3, default=list)
    only_lab = models.BooleanField(default=False)
    rgb = models.CharField("RGB", default="rgb(255, 255, 255)", null=True)

    def __str__(self):
        return str(self.sample_name)

    objects = models.Manager()


class SpectralNumber(models.Model):
    """Saves info regarding the filter and spectral number for a specific color"""

    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, primary_key=True)
    created_at = models.DateField("Creation Date", auto_now_add=True)
    updated_at = models.DateField("Update Date", auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        null=True,
        related_name="spectral_numbers",
    )
    spectral_number = ArrayField(
        models.FloatField(max_length=20), size=36, default=list
    )

    FILTER_CHOICES = [
        ("M0", "M0"),
        ("M1", "M1"),
        ("M2", "M2"),
        ("M3", "M3"),
    ]

    filter = models.CharField(
        max_length=2,
        choices=FILTER_CHOICES,
        default="M0",
    )

    objects = models.Manager()
