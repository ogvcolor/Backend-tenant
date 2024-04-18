"""Module providing a way to create a unique id"""

import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from login.models import CustomUser


class Color(models.Model):
    """Class representing color information"""

    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, primary_key=True)
    creationDate = models.DateField("Creation Date", auto_now_add=True)
    updateDate = models.DateField("Update Date", auto_now=True)
    sampleName = models.CharField("Sample Name", max_length=100)
    sampleId = models.IntegerField("Sample Id")
    isGlobal = models.BooleanField(default=True)
    userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=20)
    description = models.CharField(max_length=200, null=True, blank=True)
    Lab = ArrayField(models.FloatField(max_length=20), size=3, default=list)
    onlyLab = models.BooleanField(default=False)
    rgb = models.CharField("RGB", default="rgb(255, 255, 255)", null=True)

    def __str__(self):
        return str(self.sampleName)


class SpectralNumber(models.Model):
    """Saves info regarding the filter and spectral number for a specific color"""

    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, primary_key=True)
    created_at = models.DateField("Creation Date", auto_now_add=True)
    updated_at = models.DateField("Update Date", auto_now=True)
    userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    colorId = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        null=True,
        related_name="spectral_numbers",
    )
    spectralNumber = ArrayField(models.FloatField(max_length=20), size=36, default=list)

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
