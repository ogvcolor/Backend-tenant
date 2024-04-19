"""
    Padrão do Django
"""

from django.contrib import admin

from .models import ChartProof, Reference, Result, Tolerance


class ReferenceAdmin(admin.ModelAdmin):
    """
    Reference
    """

    list_display = [
        "id",
        "name",
        "created_at",
        "updated_at",
        "user",
        "illuminant",
        "observer",
        "filter",
    ]


class ChartProofAdmin(admin.ModelAdmin):
    """
    Chart Proof
    """

    list_display = [
        "id",
        "name",
        "created_at",
        "updated_at",
        "user",
        "rows",
        "columns",
    ]


class ToleranceAdmin(admin.ModelAdmin):
    """
    Tolerance
    """

    list_display = [
        "id",
        "name",
        "user",
        "created_at",
        "updated_at",
        "paper",
        "average",
        "maximum",
        "primary_maximum",
        "average_H",
        "primary_maximum_H",
        "CMYK",
        "secondary",
    ]


class ResultAdmin(admin.ModelAdmin):
    """
    ComparisonResult
    """

    list_display = [
        "id",
        "name",
        "user",
        "created_at",
        "updated_at",
        "tolerance",
        "reference",
        "paper",
        "average",
        "maximum",
        "primary_maximum",
        "average_H",
        "primary_maximum_H",
        "average_H",
        "secondary",
        "comment",
    ]


admin.site.register(Reference, ReferenceAdmin)
admin.site.register(ChartProof, ChartProofAdmin)
admin.site.register(Tolerance, ToleranceAdmin)
admin.site.register(Result, ResultAdmin)
