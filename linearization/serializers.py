from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from .models import CalibrationProject, ColorSet, Measured, TargetSet


class TargetSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetSet
        fields = "__all__"


class CalibrationProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalibrationProject
        fields = "__all__"


class ColorSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorSet
        fields = "__all__"


class MeasuredSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measured
        fields = "__all__"
