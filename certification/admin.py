# padrão do Django
from django.contrib import admin

from .models import ChartProof, CMYKDataSet, ComparisonResults, Tolerance


class CMYKDataSetAdmin(admin.ModelAdmin):
    """
    CMYK Data Set
    """

    list_display = (
        "id",
        "reference_name",
        "created_at",
        "updated_at",
        "user_id",
        "illuminant",
        "observer",
        "filter",
    )


class ChartProofAdmin(admin.ModelAdmin):
    """
    Chart Proof
    """

    list_display = (
        "id",
        "reference_name",
        "created_at",
        "updated_at",
        "user_id",
        "rows",
        "columns",
    )


class ToleranceAdmin(admin.ModelAdmin):
    """
    Tolerance
    """

    list_display = (
        "id",
        "name",
        "user_id",
        "created_at",
        "updated_at",
        "paper",
        "average",
        "maximum",
        "primary_maximum",
        "CMYK",
        "secondary",
    )


class ComparisonResultsAdmin(admin.ModelAdmin):
    """
    ComparisonResults
    """

    list_display = (
        "id",
        "name",
        "user_id",
        "created_at",
        "updated_at",
        "tolerance",
        "cmyk_dataset",
        "paper",
        "average",
        "maximum",
        "primary_maximum",
        "CMYK",
        "secondary",
    )


admin.site.register(CMYKDataSet, CMYKDataSetAdmin)
admin.site.register(ChartProof, ChartProofAdmin)
admin.site.register(Tolerance, ToleranceAdmin)
admin.site.register(ComparisonResults, ComparisonResultsAdmin)
