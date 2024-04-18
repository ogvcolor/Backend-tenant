# pylint: disable=no-member

import matplotlib.pyplot as plt
import numpy as np
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from knox.auth import TokenAuthentication
from numpy.polynomial.polynomial import Polynomial
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from scipy.interpolate import interp1d, lagrange, make_interp_spline

from .models import CalibrationProject, ColorSet, MeasuredValues, TargetSet
from .serializers import (CalibrationProjectSerializer, ColorSetSerializer,
                          MeasuredValuesSerializer, TargetSetSerializer)


class LinearizationView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        nominal = np.array(data.get("nominal"))
        target = np.array(data.get("target"))
        measured = np.array(data.get("measured"))

        # target
        x_black_target = np.array(nominal)
        y_black_target = np.array(target)

        x_y_spline = make_interp_spline(x_black_target, y_black_target)
        x_black_smooth_target = np.linspace(
            x_black_target.min(), x_black_target.max(), 100
        )
        y_black_smooth_target = x_y_spline(x_black_smooth_target)

        # measured
        x_black_measured = np.array(nominal)
        y_black_measured = np.array(measured)

        x_y_spline = make_interp_spline(x_black_measured, y_black_measured)
        x_black_smooth_measured = np.linspace(
            x_black_measured.min(), x_black_measured.max(), 100
        )
        y_black_smooth_measured = x_y_spline(x_black_smooth_measured)

        data = {
            "black": {
                "x_target": x_black_smooth_target,
                "y_target": y_black_smooth_target,
                "x_measured": x_black_smooth_measured,
                "y_measured": y_black_smooth_measured,
            }
        }

        return Response(data)


class InterpolationView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        nominal = np.array(data.get("nominal"))
        target = np.array(data.get("target"))
        measured = np.array(data.get("measured"))
        novo_valor = float(data.get("novo_valor"))

        nominais_ordenados = np.sort(np.append(nominal, novo_valor))

        if measured:
            splined = make_interp_spline(nominal, target)
            splinedMeasured = make_interp_spline(nominal, measured)
            target_interp = splined(nominais_ordenados)
            target_interp_measured = splinedMeasured(nominais_ordenados)

            # Arredondando para somente 1 casa decimal
            target_interp_rounded = [round(value, 1) for value in target_interp]

            resposta = {
                "nominais_ordenados": nominais_ordenados.tolist(),
                "target": target_interp_rounded,
                "measured": target_interp_measured.tolist(),
            }
        else:
            splined = make_interp_spline(nominal, target)
            target_interp = splined(nominais_ordenados)

            # Arredondando para somente 1 casa decimal
            target_interp_rounded = [round(value, 1) for value in target_interp]

            resposta = {
                "nominais_ordenados": nominais_ordenados.tolist(),
                "target": target_interp_rounded,
            }

        return Response(resposta)


"""
    Lista todos os Target Set (ou Process Curve Set) que são default, ou seja, que não possuem userId
"""


class TargetSetListDefaultView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # __isnull busca por dados undefined ou null no banco.
        target_sets = TargetSet.objects.filter(userId__isnull=True).order_by("name")
        serializer = TargetSetSerializer(target_sets, many=True)
        return Response(serializer.data)


class TargetSetListAllView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        target_sets = TargetSet.objects.all().order_by("name")
        serializer = TargetSetSerializer(target_sets, many=True)
        return Response(serializer.data)


class TargetSetListByUserIdView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        try:
            target_sets = TargetSet.objects.filter(
                Q(user_id=user_id) | Q(user_id__isnull=True)
            ).order_by("name")
            serializer = TargetSetSerializer(target_sets, many=True)
            return Response(serializer.data)
        except TargetSet.DoesNotExist:
            return Response(
                {
                    "message": "Nenhum Target Set foi encontrado para o usuário com o ID fornecido"
                },
                status=404,
            )


class TargetSetListOnlyByUserIdView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        try:
            target_sets = TargetSet.objects.filter(user_id=user_id).order_by("name")
            serializer = TargetSetSerializer(target_sets, many=True)
            return Response(serializer.data)
        except TargetSet.DoesNotExist:
            return Response(
                {
                    "message": "Nenhum Target Set foi encontrado para o usuário com o ID fornecido"
                },
                status=404,
            )


class TargetSetCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        error = []

        entity = request.data

        serializer = TargetSetSerializer(data=entity)

        if not serializer.is_valid():
            for field, messages in serializer.errors.items():
                error.append({"field": field, "message": messages})

        if serializer.is_valid():
            serializer.save()

        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                "status_code": status.HTTP_200_OK,
                "message": "Successfully saved a custom Target Set",
                "data": serializer.data,
            }
        return Response(response, status=status.HTTP_201_CREATED)


class TargetSetUpdateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        try:
            project = TargetSet.objects.get(id=pk)
        except TargetSet.DoesNotExist:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Target Set not found with the provided ID",
            }
            return JsonResponse(response, status=status.HTTP_404_NOT_FOUND)

        serializer = TargetSetSerializer(instance=project, data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status_code": status.HTTP_200_OK,
                "message": "Successfully updated the Target Set",
                "data": serializer.data,
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid data provided for Target Set update",
                "errors": serializer.errors,
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)


class TargetSetDeleteView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        try:
            project = TargetSet.objects.get(id=pk)
            serializer = TargetSetSerializer(instance=project, many=False)
            project.delete()
        except TargetSetSerializer.DoesNotExist:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Color Set not found",
            }
            return JsonResponse(response, safe=False, status=404)

        response = {
            "status_code": status.HTTP_200_OK,
            "message": "Successfully deleted the Color Set",
            "data": serializer.data,
        }
        return JsonResponse(response, safe=False, status=200)


class ColorSetListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, target_set):
        try:
            # Convert target_set para um objeto TargetSet
            target_set_instance = TargetSet.objects.get(id=target_set)
            color_sets = ColorSet.objects.filter(target_set=target_set_instance)
            serializer = ColorSetSerializer(color_sets, many=True)
            return Response(serializer.data)
        except TargetSet.DoesNotExist:
            return Response({"message": "Target Set not found"}, status=404)
        except ColorSet.DoesNotExist:
            return Response(
                {"message": "No Color Set was found for the given Target Set ID"},
                status=404,
            )


class ColorSetCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        error = []

        entity = request.data
        serializer = ColorSetSerializer(data=entity)

        if not serializer.is_valid():
            for field, messages in serializer.errors.items():
                error.append({"field": field, "message": messages})

        if serializer.is_valid():
            serializer.save()

        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                "status_code": status.HTTP_200_OK,
                "message": "Successfully saved a custom Color Set",
                "data": serializer.data,
            }
        return Response(response, status=status.HTTP_201_CREATED)


class ColorSetCreateAllView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        saved_item = []
        errors = []

        for item in request.data:
            if item.get("id"):
                continue
            else:
                serializer = ColorSetSerializer(data=item)
                if not serializer.is_valid():
                    for field, messages in serializer.errors.items():
                        errors.append(
                            {
                                "field": field,
                                "messages": messages,
                                #'value': item.get(field)
                            }
                        )
                if serializer.is_valid():
                    serializer.save()
                    saved_item.append(serializer.data)
        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(saved_item, status=status.HTTP_201_CREATED)


class ColorSetUpdateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        try:
            project = ColorSet.objects.get(id=pk)
        except ColorSet.DoesNotExist:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Color Set not found with the provided ID",
            }
            return JsonResponse(response, status=status.HTTP_404_NOT_FOUND)

        serializer = ColorSetSerializer(instance=project, data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status_code": status.HTTP_200_OK,
                "message": "Successfully updated the Color Set",
                "data": serializer.data,
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid data provided for Color Set update",
                "errors": serializer.errors,
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)


class ColorSetDeleteView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        try:
            color_set = ColorSet.objects.get(id=pk)
            serializer = ColorSetSerializer(instance=color_set, many=False)
            color_set.delete()
            response_data = {
                "status_code": status.HTTP_200_OK,
                "message": "Successfully deleted the Color Set",
                "data": serializer.data,
            }
            return JsonResponse(response_data, status=200)
        except ColorSet.DoesNotExist:
            response_data = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Color Set not found",
            }
            return JsonResponse(response_data, status=404)


class CalibrationListAllView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        projects = CalibrationProject.objects.all().order_by("calibration_project")
        serializer = CalibrationProjectSerializer(projects, many=True)
        return Response(serializer.data)


class CalibrationListByUserIdView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, userId):
        try:
            projects = CalibrationProject.objects.filter(userId=userId).order_by("name")
            serializer = CalibrationProjectSerializer(projects, many=True)
            return Response(serializer.data)
        except CalibrationProjectSerializer.DoesNotExist:
            return Response(
                {
                    "message": "Nenhum Projeto foi encontrado para o usuário com o ID fornecido"
                },
                status=404,
            )


class CalibrationCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        error = []

        serializer = CalibrationProjectSerializer(data=request.data)

        if not serializer.is_valid():
            for field, messages in serializer.errors.items():
                error.append({"field": field, "message": messages})

        if serializer.is_valid():
            serializer.save()

        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "Successfully created the project",
                "data": serializer.data,
            }
        return Response(response, status=status.HTTP_201_CREATED)


class CalibrationUpdateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        try:
            project = CalibrationProject.objects.get(id=pk)
        except CalibrationProject.DoesNotExist:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Calibration not found with the provided ID",
            }
            return JsonResponse(response, status=status.HTTP_404_NOT_FOUND)

        serializer = CalibrationProjectSerializer(instance=project, data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status_code": status.HTTP_200_OK,
                "message": "Successfully updated the project",
                "data": serializer.data,
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid data provided for project update",
                "errors": serializer.errors,
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)


class CalibrationDeleteView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        try:
            project = CalibrationProject.objects.get(id=pk)
            serializer = CalibrationProjectSerializer(instance=project, many=False)
            project.delete()
        except CalibrationProjectSerializer.DoesNotExist:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Project not found",
            }
            return JsonResponse(response, safe=False, status=404)

        response = {
            "status_code": status.HTTP_200_OK,
            "message": "Successfully deleted the project",
            "data": serializer.data,
        }
        return JsonResponse(response, safe=False, status=200)


class MeasuredListAllView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        measured_values = MeasuredValues.objects.all()
        serializer = MeasuredValuesSerializer(measured_values, many=True)
        return Response(serializer.data)


class MeasuredListByUserIdView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, calibration_project):
        try:
            measured_values = MeasuredValues.objects.filter(
                calibration_project=calibration_project
            ).order_by("name")
            serializer = MeasuredValuesSerializer(measured_values, many=True)
            return Response(serializer.data)
        except MeasuredValuesSerializer.DoesNotExist:
            return Response(
                {
                    "message": "No measured values were found for the given calibration project"
                },
                status=404,
            )


class MeasuredCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        error = []

        entity = request.data
        serializer = MeasuredValuesSerializer(data=entity)

        if not serializer.is_valid():
            for field, messages in serializer.errors.items():
                error.append({"field": field, "message": messages})

        if serializer.is_valid():
            serializer.save()

        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                "status_code": status.HTTP_200_OK,
                "message": "Successfully saved a measured values",
                "data": serializer.data,
            }
        return Response(response, status=status.HTTP_201_CREATED)


class MeasuredUpdateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        try:
            project = MeasuredValues.objects.get(id=pk)
        except MeasuredValues.DoesNotExist:
            response = {
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Measured Values not found with the provided ID",
            }
            return JsonResponse(response, status=status.HTTP_404_NOT_FOUND)

        serializer = MeasuredValuesSerializer(instance=project, data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status_code": status.HTTP_200_OK,
                "message": "Successfully updated the measured values",
                "data": serializer.data,
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid data provided for measured values update",
                "errors": serializer.errors,
            }
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)
