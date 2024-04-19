# pylint: disable=no-member
from django.http import JsonResponse
from django.shortcuts import render
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ReadData, RequestData
from .serializers import ReadDataSerializer, RequestDataSerializer


class GetMeasureRequestById(APIView):
    """Gets request for a measure"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        """GET"""
        color = RequestData.objects.get(id=pk)
        serializer = RequestDataSerializer(color, many=False)
        return Response(serializer.data)


class GetAllMeasureResponse(generics.ListAPIView):
    """List all Measure Responses (Admin Endpoint)"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ReadData.objects.all()
    serializer_class = ReadDataSerializer


class GetMeasureResponseById(APIView):
    """Gets response for measure by Id"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        """GET"""
        try:
            response = ReadData.objects.filter(request_data=pk)
            serializer = ReadDataSerializer(response, many=True)
            return Response(serializer.data)
        except ReadData.DoesNotExist:
            return Response(
                {
                    "message": "Nenhuma dado encontrada para o Request com o ID fornecido"
                },
            )


class CreateMeasureRequest(APIView):
    """
    Creates a request for measure to the local application
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """POST"""
        errors = []
        serializer = RequestDataSerializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.save()
        else:
            for field, messages in serializer.errors.items():
                errors.append({"field": field, "messages": messages})
            return Response(
                {"error": errors, "status_code": status.HTTP_400_BAD_REQUEST}
            )

        return Response(
            {
                "status_code": status.HTTP_201_CREATED,
                "message": "Successfully created the request for a measurement",
                "data": serializer.data,
            }
        )


class DeleteMeasureRequest(APIView):
    """Delete Measure Request"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        """DELETE"""
        try:
            request = RequestData.objects.get(id=pk)
            request.delete()
        except RequestData.DoesNotExist:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "request not found",
            }
            return JsonResponse(response, safe=False, status=status.HTTP_404_NOT_FOUND)

        # Return success response without serializer data
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "Successfully deleted the request",
        }
        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
