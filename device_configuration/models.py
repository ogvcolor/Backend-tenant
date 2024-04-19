# Device Configuration
import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from login.models import CustomUser

DEFAULT_MEASUREMENT_MODES = [
    ("ReflectanceSpot", "ReflectanceSpot"),
    ("ReflectanceScan", "ReflectanceScan"),
    ("DualReflectanceSpot", "DualReflectanceSpot"),
    ("DualReflectanceScan", "DualReflectanceScan"),
]


class DeviceInformation(models.Model):
    """
    Possui as configurações padrões do EyeOne que o usuário gosta, mas essa tabela possivelmente vai ser deletada
    """

    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    created_on = models.DateField("Creation Date", auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    current_device = models.BooleanField("Current Device", default=False)
    device_name = models.CharField("Device Name", max_length=100)
    device_serial = models.CharField("Device Serial", max_length=100)
    measurement_mode = models.CharField("Measurement Mode", max_length=100)


class RequestData(models.Model):
    """
    Faz chamadas para o programa local com as informações a serem medidas no EyeOne
    """

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    module_name = models.CharField(max_length=100, unique=False)
    rows = models.IntegerField(default=0)
    columns = models.IntegerField(default=0)
    measurement_mode = models.CharField(
        "Measurement Mode",
        max_length=100,
        choices=DEFAULT_MEASUREMENT_MODES,
        default="ReflectanceSpot",
    )

    objects = (
        models.Manager()
    )  # Adiciona explicitamente o gerenciador de objetos 'objects' para que o Pylint não fique frescando dizendo que não tem objects em views.py


class ReadData(models.Model):
    """
    Tabela que recebe os dados lidos diretamente do EyeOne
    """

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    density_number = ArrayField(models.FloatField(max_length=20), size=4, default=list)
    m0 = ArrayField(
        models.FloatField(max_length=20),
        default=list,
        null=True,
        blank=True,
    )
    m1 = ArrayField(
        models.FloatField(max_length=20),
        default=list,
        null=True,
        blank=True,
    )
    m2 = ArrayField(
        models.FloatField(max_length=20),
        default=list,
        null=True,
        blank=True,
    )
    request_data = models.ForeignKey(RequestData, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
