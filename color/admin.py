from django.contrib import admin

from .models import Color


class ColorAdmin(admin.ModelAdmin):
    """
    Colunas visíveis no Dashboard Django do admin
    """

    list_display = ("id", "sample_name", "user", "lab")


admin.site.register(Color, ColorAdmin)
