# biblio principal contendo as fórmulas
import colour

# import matplotlib.pyplot as plt
import numpy as np
from knox.auth import TokenAuthentication

# from numpy.polynomial.polynomial import Polynomial
# from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# from scipy.interpolate import interp1d, lagrange, make_interp_spline

# Constants for calculation
wavelengths = colour.SpectralShape(380, 730, 10)
observer = colour.MSDS_CMFS["CIE 1931 2 Degree Standard Observer"]
illuminant_D50 = colour.SDS_ILLUMINANTS["D50"]
illuminant_D65 = colour.SDS_ILLUMINANTS["D65"]
D50 = colour.colorimetry.datasets.CCS_ILLUMINANTS[
    "CIE 1931 2 Degree Standard Observer"
]["D50"]


# Common function for LAB calculation
def calculate_lab(spectral_data, illuminant):
    """
    Recebe dados espectrais e o iluminante para retornar uma lista com o LAB
    """
    sd = colour.SpectralDistribution(spectral_data, wavelengths)
    to_XYZ = colour.sd_to_XYZ(sd, observer, illuminant)
    to_XYZ_organized = np.array([x / 100 for x in to_XYZ])
    to_LAB = colour.XYZ_to_Lab(to_XYZ_organized, D50)
    return to_LAB


def calculate_RGB(spectral_data, illuminant=illuminant_D65):
    """
    Recebe dados espectrais e, caso tenha, o iluminante e retorna uma lista com valores RGB
    """
    sd = colour.SpectralDistribution(spectral_data, wavelengths)
    to_XYZ = np.array(colour.sd_to_XYZ(sd, observer, illuminant))
    to_XYZ_organized = [x / 100 for x in to_XYZ]
    to_RGB = colour.XYZ_to_RGB(to_XYZ_organized, "sRGB")
    RGB_255_scale = np.clip(np.round(to_RGB * 255), 0, 255).astype(int)
    return RGB_255_scale


def cmyk_to_rgb(data):
    """
    Converte valores de uma lista CMYK para uma lista RGB
    """
    to_number = np.array([int(value) for value in data])
    to_CMY = colour.CMYK_to_CMY(to_number)
    to_RGB = colour.CMY_to_RGB(to_CMY)
    return to_RGB


# Receives an array containing 26 spectral data and returns the LAB from it
class GetLabView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        to_LAB = calculate_lab(request.data, illuminant_D50)
        return Response(to_LAB)


class GetLabAllView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        saved_item = [
            calculate_lab(item["spectralNumber"], illuminant_D50)
            for item in request.data
        ]
        return Response(saved_item)


class GetLchabView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        to_LCHab = colour.Lab_to_LCHab(request.data)
        return Response(to_LCHab)


class GetRgbView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, illuminant=illuminant_D65):
        sd = colour.SpectralDistribution(request.data, wavelengths)
        to_XYZ = np.array(colour.sd_to_XYZ(sd, observer, illuminant))
        to_XYZ_organized = [x / 100 for x in to_XYZ]
        to_RGB = colour.XYZ_to_RGB(to_XYZ_organized, "sRGB")
        RGB_255_scale = np.clip(np.round(to_RGB * 255), 0, 255).astype(int)
        return Response(RGB_255_scale)


class GetRgbAllView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, illuminant=illuminant_D65):
        saved_item = [calculate_RGB(item["spectralNumber"]) for item in request.data]
        return Response(saved_item)


class GetCMYKtoRGBAllView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        saved_item = [cmyk_to_rgb(item) for item in request.data]
        return Response(saved_item)


class GetDeltaEView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Receberá dois arrays contendo os valores espectrais. Pra vc ver como funciona, chamei cada array de data1 e data2.
        # esses métodos primeiro convertem em XYZ, depois calculam o LAB e depois verificam o DeltaE utilizando os dois LABs blza?
        labRED = calculate_lab(request.data1, illuminant_D50)
        labYELLOW = calculate_lab(request.data2, illuminant_D50)
        deltaE2000 = colour.delta_E(labRED, labYELLOW, method="CIE 2000")
        return Response(deltaE2000)


class GetMaxDeltaEView(APIView):
    """
    Recebe dois arrays de valores espectrais e um valor referente ao DeltaE máximo.
    Gera um novo array de dados espectrais que é a diferença entre cada um dos elementos dos dois arrays do request.

    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # diferença entre cada número espectral das duas listas
        tinta = request.data.get("tinta")
        papel = request.data.get("papel")
        max_deltae = request.data.get("max_deltae")
        diferenca = [b - a if b - a > 0 else 0 for a, b in zip(tinta, papel)]

        # lista1 Lab calculation
        lab_tinta = calculate_lab(tinta, illuminant_D50)

        min_diff, best_lab, best_spectral_numbers = float("inf"), [], []

        for base in np.arange(-75, 0, 0.05):
            porcentagem = base / 75 * 100
            nova_lista = [
                (a * porcentagem) / 100 + b if (a * porcentagem) / 100 + b > 0 else 0
                for a, b in zip(diferenca, tinta)
            ]
            lab_new = calculate_lab(nova_lista, illuminant_D50)
            result = colour.delta_E(lab_tinta, lab_new, method="CIE 2000")

            if result <= max_deltae:
                min_diff, best_lab, best_spectral_numbers = result, lab_new, nova_lista
                break

        return Response(
            {
                "deltaE": min_diff,
                "Lab": best_lab,
                "spectralNumbers": best_spectral_numbers,
            }
        )


class GetMinDeltaEView(APIView):
    """
    Recebe dois arrays de valores espectrais e um valor referente ao DeltaE máximo.
    Gera um novo array de dados espectrais que é a diferença entre cada um dos elementos dos dois arrays do request.

    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        POST
        """
        tinta = request.data.get("tinta")
        papel = request.data.get("papel")
        min_deltae = request.data.get("min_deltae")
        diferenca = [b - a if b - a > 0 else 0 for a, b in zip(tinta, papel)]
        lab_tinta = calculate_lab(tinta, illuminant_D50)

        min_diff, best_lab, best_spectral_numbers = float("inf"), [], []

        base = 1
        for i in np.arange(1, 10000):
            porcentagem = base / 75
            nova_lista = [
                (a * porcentagem) + b if (a * porcentagem) / 100 + b > 0 else 0
                for a, b in zip(diferenca, tinta)
            ]
            lab_new = calculate_lab(nova_lista, illuminant_D50)
            result = colour.delta_E(lab_tinta, lab_new, method="CIE 2000")

            if result <= min_deltae:
                min_diff, best_lab, best_spectral_numbers = result, lab_new, nova_lista
            if result > min_deltae:
                break

            base = base + 0.05

        return Response(
            {
                "deltaE": min_diff,
                "Lab": best_lab,
                "spectralNumbers": best_spectral_numbers,
            }
        )


class GetDeltaEHfromLabView(APIView):
    """
    Recebe dois conjuntos de Lab, da amostra e da referência (DataSet), e retorna o DeltaE entre os dois
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        POST
        """
        sample_data = request.data.get("sample")
        reference_data = request.data.get("reference")
        delta_es = []
        delta_hs = []

        for sample_item, reference_item in zip(sample_data, reference_data):
            lab_sample = sample_item.get("lab")
            lab_reference = reference_item.get("lab")
            delta_e = colour.delta_E(lab_sample, lab_reference, method="CIE 2000")
            delta_es.append(delta_e)

            lch_sample = colour.Lab_to_LCHab(lab_sample)
            lch_reference = colour.Lab_to_LCHab(lab_reference)

            a1, b1 = lch_sample[..., 1], lch_sample[..., 2]
            a2, b2 = lch_reference[..., 1], lch_reference[..., 2]

            deltah = abs(((b2 - b1) - 180) % 360 - 180)
            delta_hs.append(deltah)

        return Response(
            {
                "delta_es": delta_es,
                "delta_hs": delta_hs,
            }
        )
