"""
    Certification Serializer
"""

from rest_framework import serializers

from .models import ChartProof, CMYKData, Reference, Result, Tolerance


class CMYKDataSerializer(serializers.ModelSerializer):
    """
    CMYK Data Serializer
    """

    class Meta:
        """
        Meta
        """

        model = CMYKData
        fields = "__all__"


class ReferenceSerializer(serializers.ModelSerializer):
    """
    CMYK DataSet Serializer
    """

    cmyk_data = CMYKDataSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta
        """

        model = Reference
        fields = "__all__"


class ChartProofSerializer(serializers.ModelSerializer):
    """
    Chart Proof Serializer
    """

    cmyk_data = CMYKDataSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta
        """

        model = ChartProof
        fields = "__all__"


class ToleranceSerializer(serializers.ModelSerializer):
    """
    Evaluation Method Serializer
    """

    class Meta:
        """
        Meta
        """

        model = Tolerance
        fields = "__all__"


class ResultSerializer(serializers.ModelSerializer):
    """
    Results Serializer
    """

    cmyk_data = CMYKDataSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta
        """

        model = Result
        fields = "__all__"
