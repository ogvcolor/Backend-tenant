# pylint: disable=no-member
from django.http import JsonResponse
from knox.auth import TokenAuthentication
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Color
from .serializers import ColorSerializer, SpectralNumberSerializer

# Create your views here.


@api_view(["GET"])
def api_over_view(request):
    """Show color endpoints"""
    api_urls = {
        "Colors": "/color-list",
        "Color View": "/color-detail/<str:pk>/",
        "Create Color": "/color-create/",
        "Update Color": "/color-update/<str:pk>/",
        "Delete Color": "/color-delete/<str:pk>/",
    }

    return Response(api_urls)


class ColorListAllView(generics.ListAPIView):
    """List all Colors (Admin Endpoint)"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Color.objects.all().order_by("sample_name")
    serializer_class = ColorSerializer


class ColorListView(APIView):
    """List all colors where isGlobal = True"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """GET"""
        colors = Color.objects.filter(is_global=True).order_by("sample_name")
        serializer = ColorSerializer(colors, many=True)
        return Response(serializer.data)


class ColorListByUserIdView(APIView):
    """List all colors associated with the user_id"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        """GET"""
        try:
            user_colors = Color.objects.filter(user=user_id).order_by("sample_name")
            serializer = ColorSerializer(user_colors, many=True)
            return Response(serializer.data)
        except Color.DoesNotExist:
            return Response(
                {"message": "Nenhuma cor encontrada para o usuário com o ID fornecido"},
                status=404,
            )


class ColorDetailView(APIView):
    """Gets color information"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        """GET"""
        color = Color.objects.get(id=pk)
        serializer = ColorSerializer(color, many=False)
        return Response(serializer.data)


class ColorCreateView(APIView):
    """Create one color"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """POST"""
        error = []
        serializer = ColorSerializer(data=request.data)

        if serializer.is_valid():
            # Salvar a instância de Color
            color_instance = serializer.save()

            # Verificar se há dados de spectralNumbers no request
            spectral_numbers_data = request.data.get("spectralNumbers", [])

            # Criar instâncias de SpectralNumber associadas à instância de Color criada acima
            for data in spectral_numbers_data:
                spectral_number_serializer = SpectralNumberSerializer(data=data)
                if spectral_number_serializer.is_valid():
                    spectral_number_serializer.save(
                        user=request.user, color=color_instance
                    )
                else:
                    error.append(
                        {
                            "field": "spectral_numbers",
                            "message": spectral_number_serializer.errors,
                        }
                    )

            if error:
                return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Serializar a instância de Color com os dados dos spectralNumbers
                color_with_spectral_numbers_serializer = ColorSerializer(color_instance)
                response_data = color_with_spectral_numbers_serializer.data

                response = {
                    "status_code": status.HTTP_201_CREATED,
                    "message": "Successfully created the color with associated spectral numbers",
                    "data": response_data,
                }
                return Response(response, status=status.HTTP_201_CREATED)
        else:
            for field, messages in serializer.errors.items():
                error.append({"field": field, "message": messages})
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)


class ColorCreateAllView(APIView):
    """Create more than one color"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """POST"""
        saved_items = []
        errors = []

        for item in request.data:
            color_serializer = ColorSerializer(data=item)
            if color_serializer.is_valid():
                color_instance = color_serializer.save()

                spectral_numbers_data = item.get("spectralNumbers", {})

                for data in spectral_numbers_data:
                    spectral_number_serializer = SpectralNumberSerializer(data=data)
                    if spectral_number_serializer.is_valid():
                        spectral_number_serializer.save(
                            userId=request.user, color=color_instance
                        )
                    else:
                        errors.append(
                            {
                                "field": "spectral_numbers",
                                "message": spectral_number_serializer.errors,
                            }
                        )

                saved_items.append(
                    {
                        "color": color_serializer.data,
                        "spectral": spectral_number_serializer.data,
                    }
                )
            else:
                for field, messages in color_serializer.errors.items():
                    errors.append({"field": field, "messages": messages})

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(saved_items, status=status.HTTP_201_CREATED)


class ColorUpdateView(APIView):
    """Update a color"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        """PATCH"""
        try:
            color = Color.objects.get(id=pk)
        except Color.DoesNotExist:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Color not found with the provided ID",
            }
            return JsonResponse(response, status=status.HTTP_404_NOT_FOUND)

        serializer = ColorSerializer(instance=color, data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status_code": status.HTTP_200_OK,
                "message": "Successfully updated the color",
                "data": serializer.data,
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid data provided for color update",
                "errors": serializer.errors,
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)


class ColorDeleteView(APIView):
    """Delete Color"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        """DELETE"""
        try:
            color = Color.objects.get(id=pk)
            color.delete()
        except Color.DoesNotExist:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Color not found",
            }
            return JsonResponse(response, safe=False, status=status.HTTP_404_NOT_FOUND)

        # Return success response without serializer data
        response = {
            "status_code": status.HTTP_200_OK,
            "message": "Successfully deleted the color",
        }
        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
