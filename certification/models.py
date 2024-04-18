import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from login.models import CustomUser


class CMYKDataSet(models.Model):
    """
    Contém os valores CMYK padrão de acordo com o 'CMYK Characterization Data' do site color.org
    """

    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, primary_key=True)
    reference_name = models.CharField(max_length=100, unique=True)  # Ex. FOGRA39
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    illuminant = models.CharField(null=True, blank=True)
    observer = models.CharField(null=True, blank=True)

    FILTER_CHOICES = [
        ("M0", "M0"),
        ("M1", "M1"),
        ("M2", "M2"),
        ("M3", "M3"),
    ]

    filter = models.CharField(
        max_length=2,
        choices=FILTER_CHOICES,
        default="M0",
    )

    objects = (
        models.Manager()
    )  # Adiciona explicitamente o gerenciador de objetos 'objects' para que o Pylint não fique frescando dizendo que não tem objects


class ChartProof(models.Model):
    """
    Contém os valores CMYK para renderização dos charts que são utilizados como prova
    """

    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, primary_key=True)
    reference_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    rows = models.IntegerField(default=0)
    columns = models.IntegerField(default=0)
    objects = (
        models.Manager()
    )  # Adiciona explicitamente o gerenciador de objetos 'objects' para que o Pylint não fique frescando dizendo que não tem objects


class Tolerance(models.Model):
    """
    Contém os dados relacionados aos métodos de Avaliação como valores de tolerância e também os DeltaE relacionados a cada um deles. Por isso formato JSON
    """

    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, primary_key=True)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paper = models.JSONField(
        max_length=20
    )  # ex: { "value": 3, "deltae": "DeltaE 2000" } - Este exemplo vale para todos
    average = models.JSONField(max_length=20)
    maximum = models.JSONField(max_length=20)
    primary_maximum = models.JSONField(max_length=20)
    CMYK = models.JSONField(max_length=20)  # Terá sempre a ordem de CMYK!
    secondary = models.JSONField(
        max_length=20
    )  # Terá sempre a ordem: vermelho, verde, azul (RGB)

    objects = (
        models.Manager()
    )  # Adiciona explicitamente o gerenciador de objetos 'objects' para que o Pylint não fique frescando dizendo que não tem objects


class ComparisonResults(models.Model):
    """
    Contém os valores do resultado da comparação dos dados das cores do usuário e os padrões do CMYKDataSet, assim como os dados CMYK do usuário
    """

    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, primary_key=True)
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100, unique=True)
    tolerance = models.ForeignKey(
        Tolerance, on_delete=models.DO_NOTHING, null=False
    )  # Se deletar o evaluation_method, não vai deletar os resultados, mas ao renderizar, vai aparecer nenhum valor de tolerância
    cmyk_dataset = models.ForeignKey(
        CMYKDataSet,
        on_delete=models.DO_NOTHING,
        null=False,
        default="f6e6bbfe-60a7-4a4e-90a9-b75dbbc9a1ef",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paper = models.FloatField(max_length=20)
    average = models.FloatField(max_length=20)
    maximum = models.FloatField(max_length=20)
    primary_maximum = models.FloatField(max_length=20)
    CMYK = ArrayField(models.FloatField(max_length=20), size=4, default=list)
    secondary = ArrayField(models.FloatField(max_length=20), size=3, default=list)

    objects = (
        models.Manager()
    )  # Adiciona explicitamente o gerenciador de objetos 'objects' para que o Pylint não fique frescando dizendo que não tem objects


class CMYKData(models.Model):
    """
    Contém os dados referentes aos valores CMYK, assim como o Lab
    """

    id = models.UUIDField(default=uuid.uuid4, null=False, blank=False, primary_key=True)
    reference_name = models.CharField(max_length=100)  # Ex. 000-010-000-000
    sample_id = models.CharField(max_length=100, null=True)
    sample_name = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cmyk = ArrayField(models.FloatField(max_length=20), size=4, default=list)
    lab = ArrayField(models.FloatField(max_length=20), size=3, default=list, null=True)
    rgb = models.CharField("RGB", default="rgb(255, 255, 255)", null=True)
    chart_proof = models.ForeignKey(
        ChartProof,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cmyk_data",
    )
    cmyk_dataset = models.ForeignKey(
        CMYKDataSet,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cmyk_data",
    )
    comparison_results = models.ForeignKey(
        ComparisonResults,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cmyk_data",
    )

    objects = (
        models.Manager()
    )  # Adiciona explicitamente o gerenciador de objetos 'objects' para que o Pylint não fique frescando dizendo que não tem objects
