import re

from django.http import JsonResponse
from django.shortcuts import render
from knox.auth import TokenAuthentication
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from data_processing.services import (
    DataProcessingServices,
    StandardDataProcessingServices,
)


class AnalyseData(viewsets.ViewSet):
    """
    Primeira entrada do input para chamada do Service para que o processamento do .txt seja feito
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=["post"])
    def analysis(self, request):
        """
        Verifica se o .txt está no formato string para processar pelo Service
        """
        try:
            data_processor = DataProcessingServices()
            data = data_processor.data_filtering(request.data)

            # Error
            if isinstance(
                data, str
            ):  # Se data é uma string, então ocorreu um erro no serviço
                # Lógica para lidar com o erro, como por exemplo, retornar um código de erro específico ou logar o erro
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": data,
                }
                return JsonResponse(response, safe=False, status=400)

            # Lógica para o caso de sucesso
            response = {
                "status_code": status.HTTP_200_OK,
                "message": "Ok",
                "data": data,
            }
            return JsonResponse(response, safe=False, status=200)
        except ImportError as e:

            # Error
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": str(e),
            }
            return JsonResponse(response, safe=False)

    @action(detail=False, methods=["post"])
    def standard_analysis(self, request):
        """
        Verifica se o .txt está no formato string para processar pelo Service
        """
        try:
            # Create an instance of StandardataProcessingServices
            data_processor = StandardDataProcessingServices()

            # Call data_filtering method on the instance and pass request.data
            data = data_processor.data_filtering(request.data)

            # Error
            if isinstance(
                data, str
            ):  # Se data é uma string, então ocorreu um erro no serviço
                # Lógica para lidar com o erro, como por exemplo, retornar um código de erro específico ou logar o erro
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": data,
                }
                return JsonResponse(response, safe=False, status=400)

            # Lógica para o caso de sucesso
            response = {
                "status_code": status.HTTP_200_OK,
                "message": "Ok",
                "data": data,
            }
            return JsonResponse(response, safe=False, status=200)
        except ImportError as e:

            # Error
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": str(e),
            }
            return JsonResponse(response, safe=False)
