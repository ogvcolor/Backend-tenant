from django.contrib import admin
from .models import CalibrationProject, TargetSet

# Register your models here.
admin.site.register(CalibrationProject)
admin.site.register(TargetSet)