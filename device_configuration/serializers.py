from rest_framework import serializers

from .models import ReadData, RequestData


class ReadDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadData
        fields = "__all__"


class RequestDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestData
        fields = "__all__"
