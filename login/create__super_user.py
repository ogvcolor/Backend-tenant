# Em algum arquivo `management/commands/create_tenant_superuser.py`

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django_tenants.utils import schema_context
from app.models import Client


class Command(BaseCommand):
    help = 'Cria um superusuário para cada tenant'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        tenants = Client.objects.all()


        for teste in tenants:
            with schema_context(teste.schema_name):
                email = 'superuser@example.com'  # Substitua pelo email desejado
                password = 'superuserpassword'    # Substitua pela senha desejada
                User.objects.create_superuser(email, password)
                self.stdout.write(self.style.SUCCESS(f'Superusuário criado para {teste.name}'))
