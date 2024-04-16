

from django_tenants.models import TenantMixin, DomainMixin
from django.db import models

import uuid
import os
from django_tenants.postgresql_backend.base import _check_schema_name

class Client (TenantMixin):
    name = models.CharField (max_length=100, unique=True, null=False, blank=False)
    created_on = models.DateField (auto_now_add =True)
    tenant_uuid = models.UUIDField(default=uuid.uuid4, null=False, blank=False)
    paid_until = models.DateField() #value has an invalid date format. It must be in YYYY-MM-DD format.
    on_trial = models.BooleanField(default=False)
    language = models.CharField(max_length=100, null=False, blank=False, default='pt_BR')
    domain_url = models.URLField(blank=True, null=True, default=os.getenv("DOMAIN"))
    domain_url = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Construa a URL com base no nome do domínio
        if self.domain_url is None:
            # Se domain_url não estiver definido, use o valor da variável de ambiente DOMAIN
            domain = os.environ["DOMAIN"]
            if domain is not None:
                self.domain_url = f"http://{domain}.localhost:8000"

        # Chame o método save() da classe pai para salvar o modelo
        super().save(*args, **kwargs)

        
class Domain (DomainMixin):
    pass