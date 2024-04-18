from rest_framework import serializers

from .models import Color, SpectralNumber


class SpectralNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpectralNumber
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    """
    Color Serializer where Spectral Number associated is called as well
    """

    spectral_numbers = SpectralNumberSerializer(many=True, read_only=True)

    class Meta:
        model = Color
        fields = "__all__"
