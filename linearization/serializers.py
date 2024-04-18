from .models import TargetSet, CalibrationProject, ColorSet, MeasuredValues
from rest_framework import serializers
from datetime import datetime
from django.utils import timezone


class TargetSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetSet
        fields = '__all__'
        

class CalibrationProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalibrationProject
        fields = '__all__'

class ColorSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorSet
        fields = '__all__'

class MeasuredValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasuredValues
        fields = '__all__'
