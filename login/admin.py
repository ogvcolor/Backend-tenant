from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfis de Usuário'

class CustomizedUserAdmin(UserAdmin):
    # Remover UserProfileInline da lista de inlines
    inlines = []
    # Removendo referências aos campos 'groups' e 'user_permissions'
    filter_horizontal = ()
    list_filter = ()




admin.site.register(CustomUser, CustomizedUserAdmin)
admin.site.register(UserProfile)
