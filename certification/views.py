# pylint: disable=no-member
from django.http import JsonResponse
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChartProof, CMYKData, Reference, Result, Tolerance
from .serializers import (
    ChartProofSerializer,
    CMYKDataSerializer,
    ReferenceSerializer,
    ResultSerializer,
    ToleranceSerializer,
)


@api_view(["GET"])
def certification_over_view():
    """Show Certification Endpoints"""
    api_urls = {
        "Get Reference": "get-reference/",
        "Get Chart Proof": "get-chart-proof/",
        "Create Reference": "create-reference/",
        "Create Tolerance Method": "create-tolerance/",
    }

    return Response(api_urls)


class ReferenceListAllView(generics.ListAPIView):
    """Lista todos os CMYK Data Set como FOGRA39"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer


class ReferenceListByUserIdView(generics.ListAPIView):
    """Lista todos os CMYK Data Set de um User"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        """GET"""
        try:
            user_data = Reference.objects.filter(user_id=user_id)
            serializer = ReferenceSerializer(user_data, many=True)
            return Response(serializer.data)
        except Reference.DoesNotExist:
            return Response(
                {
                    "message": "Nenhum CMYDataSet foi encontrado para o usuário com o ID fornecido"
                },
                status=404,
            )


class ChartProofListAllView(generics.ListAPIView):
    """Lista todos os Chart Proof como fogra Media Wedge CMYK V3.0 strip"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ChartProof.objects.all()
    serializer_class = ChartProofSerializer


class ChartProofListByUserIdView(generics.ListAPIView):
    """Lista todos os CMYK Data Set de um User"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        """GET"""
        try:
            user_data = ChartProof.objects.filter(user_id=user_id)
            serializer = ChartProofSerializer(user_data, many=True)
            return Response(serializer.data)
        except ChartProof.DoesNotExist:
            return Response(
                {
                    "message": "Nenhum Chart Proof foi encontrado para o usuário com o ID fornecido"
                },
                status=404,
            )


class CMYKDataListAllView(generics.ListAPIView):
    """Lista todos os CMYK Data Set como FOGRA39"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = CMYKData.objects.all()
    serializer_class = CMYKDataSerializer


class CMYKDataListByDataIdView(generics.ListAPIView):
    """Lista todos os CMYK Data de um User"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, data_id):
        """POST"""

        try:
            if request.data["type"] == "CMYKDataSet":
                column = "cmyk_dataset"
            else:
                column = "chart_proof"

            # Crie um dicionário para passar dinamicamente os argumentos de filtro
            filter_kwargs = {
                f"{column}": data_id,
            }

            # Use expressões de filtro dinâmicas
            data_id = CMYKData.objects.filter(**filter_kwargs)
            serializer = CMYKDataSerializer(data_id, many=True)
            return Response(serializer.data)

        except CMYKData.DoesNotExist:
            return Response(
                {
                    "message": "Nenhum CMYData foi encontrado para o usuário com o Data ID fornecido"
                },
                status=404,
            )


class ToleranceListAllView(generics.ListAPIView):
    """Lista todos os métodos de avaliação como o ISO 12647-7"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tolerance.objects.all()
    serializer_class = ToleranceSerializer


class ResultListAllView(generics.ListAPIView):
    """Lista todos os resultados de controle de qualidade como níveis de tolerância"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class CreateCMYKDataSetView(APIView):
    """
    Salva primeiramente o CMYK DataSet (ou Chart Proof) e depois faz um loop para salvar todos
    os dados CMYK, associando o respectivo ForeignKey de CMYK DataSet (ou Chart Proof)

    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """POST"""
        saved_items = []
        errors = []

        if request.data["type"] == "CMYKDataSet":
            data_set_serializer = ReferenceSerializer(data=request.data)
        else:
            data_set_serializer = ChartProofSerializer(data=request.data)

        # Serializa e salva os dados de DataSet

        if data_set_serializer.is_valid():
            saved_data = data_set_serializer.save()
        else:
            for field, messages in data_set_serializer.errors.items():
                errors.append({"field": field, "messages": messages})
            print("")
            print("")
            print("")
            print("errors", errors)

        # Serializa os dados de CMYKData
        for item in request.data["cmyk_data"]:
            cmyk_data_serializer = CMYKDataSerializer(data=item)

            if cmyk_data_serializer.is_valid():
                if request.data["type"] == "CMYKDataSet":
                    cmyk_data = cmyk_data_serializer.save(cmyk_dataset=saved_data)
                else:
                    cmyk_data = cmyk_data_serializer.save(chart_proof=saved_data)
            else:
                for field, messages in cmyk_data_serializer.errors.items():
                    errors.append({"field": field, "messages": messages})
            saved_items.append(cmyk_data)

        if errors:  # Pylint reclama que não é necessário o else, mas é sim!
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"data_set": data_set_serializer.data},
                status=status.HTTP_201_CREATED,
            )


class CreateToleranceSetView(APIView):
    """
    Salva os dados de Métodos de Avaliação, como níveis de tolerância e DeltaE associados

    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """POST"""
        error = []
        serializer = ToleranceSerializer(data=request.data)

        if serializer.is_valid():
            # Salva a instância do Tolerance
            serializer.save()

        else:
            error.append({"message": serializer.errors})

        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        else:
            response_data = serializer.data
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "Successfully created the Tolerance Method",
                "data": response_data,
            }
            return Response(response, status=status.HTTP_201_CREATED)


class CreateResultSetView(APIView):
    """
    Salva os dados de Métodos de Avaliação, como níveis de tolerância e DeltaE associados

    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """POST"""
        errors = []
        serializer = ResultSerializer(data=request.data)
        saved_items = []

        if serializer.is_valid():
            # Salva a instância do Comparision Results
            comparison_result_instance = serializer.save()

        else:
            for field, messages in serializer.errors.items():
                errors.append({"field": field, "messages": messages})
            return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Após salvar o result, salva os cmyk_data relacionados do sample
        for item in request.data["cmyk_data"]:
            cmyk_data_serializer = CMYKDataSerializer(data=item)

            if cmyk_data_serializer.is_valid():
                cmyk_data = cmyk_data_serializer.save(
                    comparison_results=comparison_result_instance
                )
            else:
                for field, messages in cmyk_data_serializer.errors.items():
                    errors.append({"field": field, "messages": messages})
            saved_items.append(cmyk_data)

        if errors:  # Pylint reclama que não é necessário o else, mas é sim!
            return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            response_data = serializer.data
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "Successfully created the Comparison Result",
                "data": response_data,
            }
            return Response(response, status=status.HTTP_201_CREATED)


class UpdateResultSetView(APIView):
    """Update a Comparison Result"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        """PATCH"""
        try:
            result = Result.objects.get(id=pk)
        except Result.DoesNotExist:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Result not found with the provided ID",
            }
            return JsonResponse(response, status=status.HTTP_404_NOT_FOUND)

        serializer = Result(instance=result, data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status_code": status.HTTP_200_OK,
                "message": "Successfully updated the Comparison Result",
                "data": serializer.data,
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid data provided for Comparison Result update",
                "errors": serializer.errors,
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)


class DeleteResultView(APIView):
    """Delete Comparison Results"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        """DELETE"""
        try:
            color = Result.objects.get(id=pk)
            color.delete()
        except Result.DoesNotExist:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Comparison Result not found",
            }
            return JsonResponse(response, safe=False, status=status.HTTP_404_NOT_FOUND)

        # Return success response without serializer data
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "Successfully deleted the Comparison Result",
        }
        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
