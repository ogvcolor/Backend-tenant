from rest_framework import serializers

from .models import ChartProof, CMYKData, CMYKDataSet, ComparisonResults, Tolerance


class CMYKDataSerializer(serializers.ModelSerializer):
    """
    CMYK Data Serializer
    """

    class Meta:
        model = CMYKData
        fields = "__all__"


class CMYKDataSetSerializer(serializers.ModelSerializer):
    """
    CMYK DataSet Serializer
    """

    cmyk_data = CMYKDataSerializer(many=True, read_only=True)

    class Meta:
        model = CMYKDataSet
        fields = "__all__"


class ChartProofSerializer(serializers.ModelSerializer):
    """
    Chart Proof Serializer
    """

    cmyk_data = CMYKDataSerializer(many=True, read_only=True)

    class Meta:
        model = ChartProof
        fields = "__all__"


class ToleranceSerializer(serializers.ModelSerializer):
    """
    Evaluation Method Serializer
    """

    class Meta:
        model = Tolerance
        fields = "__all__"


class ComparisonResultsSerializer(serializers.ModelSerializer):
    """
    Comparison Results Serializer
    """

    cmyk_data = CMYKDataSerializer(many=True, read_only=True)

    class Meta:
        model = ComparisonResults
        fields = "__all__"
