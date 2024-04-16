from django.contrib import admin
from .models import Client
from .models import Domain


admin.site.register(Client)
admin.site.register(Domain)
