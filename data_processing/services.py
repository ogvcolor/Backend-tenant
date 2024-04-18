""" Regular expression for separating double spaces etc"""

import re

import colour
import numpy as np
from colormath.color_conversions import convert_color
from colormath.color_objects import LabColor, sRGBColor

"""

    No upload do arquivo, verificar primeiro os dados espectrais, convertê-los para LAB
    e comparar com o LAB que potencialmente vem no arquivo. Se tiver diferente, alerta o usuário.

    O cálculo LAB precisa utilizar o illuminant D50 como default, mas é preciso fazer o cálculo com D60.

"""


class DataProcessingServices:
    """
    Analisa inputs que contém dados de cores para salvar na biblioteca
    """

    def data_filtering(self, uploaded_file):
        """
        Filtragem dos dados de acordo com as colunas
        """
        # header indexes variables
        header_start_index = None
        header_end_index = None
        header_values = None

        # data indexes variables
        data_start_index = None
        data_end_index = None
        number_of_sets = None
        nm_index = None

        # Sample Id and Sample Name indexes
        id_index = -1
        name_index = -1

        # Boolean variables
        has_380 = False
        unkown_data = True

        is_nm = False

        for i, line in enumerate(uploaded_file):
            if line.strip() == "BEGIN_DATA_FORMAT":
                unkown_data = False
                header_start_index = i
            elif line.strip() == "END_DATA_FORMAT":
                header_end_index = i

            if line.strip() == "BEGIN_DATA":
                data_start_index = i
            elif line.strip() == "END_DATA":
                data_end_index = i

            if "NUMBER_OF_SETS" in line.strip():
                line = re.sub(r"^\S\n\t+", "", line.strip()).split()
                number_of_sets = int(line[1])

        # Error
        if unkown_data:
            return "Unknown data format"

        # HEADER FILTERING
        if header_start_index is not None and header_end_index is not None:
            header_line = uploaded_file[header_start_index + 1 : header_end_index]

        # Error
        if not any("400" in line or "700" in line for line in header_line):
            return "No spectral data found"

        header_values = re.sub(r"(?<=\S)\s+(?=\S)", "\t", header_line[0]).split("\t")
        if not header_values[-1]:
            header_values = header_values[:-1]

        for index, value in enumerate(header_values):

            if "380" in value:
                spectral_start = index
                has_380 = True
            elif "400" in value and not has_380:
                spectral_start = index
            if "700" in value:
                spectral_end = index
            elif "730" in value and has_380:
                no_730 = False
                spectral_end = index
            if re.search(r"id", value, re.IGNORECASE):
                id_index = index
            if re.search(r"name", value, re.IGNORECASE):
                name_index = index
            if re.search(r"nm", value, re.IGNORECASE) and not is_nm:
                nm_index = index
                is_nm = True

        # DATA FILTERING
        if data_start_index is not None and data_start_index is not None:
            data_content = uploaded_file[data_start_index + 1 : data_end_index]

        # Error
        if number_of_sets != len(data_content):
            return "Number of sets is not the same as the number of colors!"

        # Calculate the effective starting index for data_content
        if id_index != -1 and name_index != -1:
            start_index = max(id_index, name_index)
        elif id_index != -1:
            start_index = id_index
        elif name_index != -1:
            start_index = name_index
        else:
            # Both id_index and name_index are -1, start from the beginning
            start_index = 0

        sample_id_list = []
        sample_name_list = []
        # First separate overall data values \t and removes sample_id and sample_name from the list, if it exists
        for index, line in enumerate(data_content):
            line = line.split("\t")
            sample_id = line[id_index] if id_index != -1 else index + 1
            sample_id_list.append(sample_id)

            sample_name = line[name_index] if name_index != -1 else ""
            sample_name_list.append(sample_name)

        if start_index != 0:
            data_content = [
                line.split("\t")[start_index + 1 :] for line in data_content
            ]
            spectral_start = spectral_start - start_index - 1
            spectral_end = spectral_end - start_index
            nm_index = nm_index - start_index - 1
        else:
            data_content = [line.split("\t")[start_index:] for line in data_content]
            spectral_start = spectral_start - start_index
            spectral_end = spectral_end - start_index + 1
            nm_index = nm_index - start_index

        # Second, removes all spaces, double spaces, tabular etc and replaces it with single space
        for row_index, row in enumerate(data_content):
            for col_index, col_value in enumerate(row):
                data_content[row_index][col_index] = re.sub(
                    r"^\S\n\t+", "", col_value.strip()
                )

        # Third, separates elements in the list that are not separated yet (specially spectral data from the -1 element in some cases)
        new_data = []
        for i in range(len(data_content)):
            split_values = [
                value for element in data_content[i] for value in element.split()
            ]
            new_data.append(split_values)

        # DATA ORGANIZATION
        # Substituing eventual comma for dot in each element
        for index, line in enumerate(new_data):
            # Substituir vírgulas por pontos em cada elemento da linha
            new_data[index] = [value.replace(",", ".") for value in line]

            # Substituir aspas duplas no nome da amostra
            sample_name_list[index] = sample_name_list[index].replace('"', "")

            # Se o índice do nome não foi encontrado, concatenar todos os números até o primeiro "nm"
            if name_index == -1:
                sample_name_list[index] = "-".join(line[start_index:nm_index])

        # Filling the start and end with (I can also use has_380 and no730 as conditionals for filling the empty elements)
        spectral_number = []
        for line in new_data:
            number = line[spectral_start:spectral_end]
            if not has_380:
                number.insert(0, "0.000")
                number.insert(0, "0.000")
                number.append("0.000")
                number.append("0.000")
                number.append("0.000")

            spectral_number.append(number)

        organized_data = []
        for index, line in enumerate(new_data):
            item = {
                "sample_id": sample_id_list[index],
                "sample_name": sample_name_list[index],
                "spectral_number": spectral_number[index],
            }

            # Error
            if len(spectral_number[index]) != 36:
                return "Incorrect number of spectral data found"

            organized_data.append(item)

        return organized_data


class StandardDataProcessingServices:
    """
    Analisa os inputs para processamento de dados do tipo FOGRA39
    """

    def data_filtering(self, uploaded_file):
        """
        Processamento do input
        """
        # header indexes variables
        header_start_index = None
        header_end_index = None
        header_values = None

        # cmyk and lab indexes variables
        cmyk_start = -1
        cmyk_end = -1
        lab_start = -1
        lab_end = -1

        spectral_start = -1

        # data indexes variables
        data_start_index = None
        data_end_index = None
        number_of_sets = None

        # Sample Id and Sample Name indexes
        id_index = -1
        name_index = -1
        has_name = False

        # Name of the input
        descriptor = ""

        # Boolean variables
        has_380 = False
        unkown_data = True

        is_nm = False

        for i, line in enumerate(uploaded_file):
            if "DESCRIPTOR" in line:
                descriptor = re.sub(r"^\S\n\t+", "", line.strip()).split()
            if line.strip() == "BEGIN_DATA_FORMAT":
                unkown_data = False
                header_start_index = i
            elif line.strip() == "END_DATA_FORMAT":
                header_end_index = i

            if line.strip() == "BEGIN_DATA":
                data_start_index = i
            elif line.strip() == "END_DATA":
                data_end_index = i

            if "NUMBER_OF_SETS" in line.strip():
                line = re.sub(r"^\S\n\t+", "", line.strip()).split()
                number_of_sets = int(line[1])

        # Error
        if unkown_data:
            return "Unknown data format"

        # HEADER FILTERING
        if header_start_index is not None and header_end_index is not None:
            header_line = uploaded_file[header_start_index + 1 : header_end_index]

        # Error if CMYK string is not included in the header
        if not any("CMYK" in line for line in header_line):
            return "No CMYK data found"

        # Searches for LAB values
        has_lab = bool(any("LAB" in line for line in header_line))

        header_values = re.sub(r"(?<=\S)\s+(?=\S)", "\t", header_line[0]).split("\t")
        if not header_values[-1]:
            header_values = header_values[:-1]

        for index, value in enumerate(header_values):
            # busca dado espectral
            if "380" in value:
                spectral_start = index
                has_380 = True
            elif "400" in value and not has_380:
                spectral_start = index
            if "700" in value:
                spectral_end = index
            elif "730" in value and has_380:
                no_730 = False
                spectral_end = index

            if "CMYK_C" in value:
                cmyk_start = index
            elif "CMYK_K" in value:
                cmyk_end = index

            if has_lab and "LAB_L" in value:
                lab_start = index
            elif has_lab and "LAB_B" in value:
                lab_end = index

            if re.search(r"id", value, re.IGNORECASE):
                id_index = index
            if re.search(r"name", value, re.IGNORECASE):
                name_index = index
                has_name = True
            if re.search(r"nm", value, re.IGNORECASE) and not is_nm:
                nm_index = index
                is_nm = True

        # DATA FILTERING
        if data_start_index is not None and data_start_index is not None:
            data_content = uploaded_file[data_start_index + 1 : data_end_index]

        # Error
        if number_of_sets != len(data_content):
            return "Number of sets is not the same as the number of colors!"

        # Calculate the effective starting index for data_content
        if id_index != -1 and name_index != -1:
            start_index = max(id_index, name_index)
        elif id_index != -1:
            start_index = id_index
        elif name_index != -1:
            start_index = name_index
        else:
            # Both id_index and name_index are -1, start from the beginning
            start_index = 0

        sample_id_list = []
        sample_name_list = []
        cmyk_data_list = []
        reference_name_list = []
        lab = []
        rgb_list = []
        for index, line in enumerate(data_content):
            line = re.sub(r"(?<=\S)\s+(?=\S)", "\t", line.strip()).split("\t")
            sample_id = line[id_index] if id_index != -1 else index + 1
            sample_id_list.append(sample_id)

            if has_name:
                sample_name = line[name_index] if name_index != -1 else ""
                sample_name_list.append(sample_name)

            # getting CMYK data
            cmyk_data = line[cmyk_start : cmyk_end + 1]
            cmyk_data_list.append(cmyk_data)

            # getting the reference_name, AKA, 000-000-1000
            reference_name = get_reference_name(cmyk_data)
            reference_name_list.append(reference_name)

            if lab_start != 1:
                lab_data = correct_lab_format(line[lab_start : lab_end + 1])

                lab.append(lab_data)

            # converting to RGB
            # to_rgb = cmyk_to_rgb(cmyk_data)

            to_rgb = lab_to_rgb(lab[index])

            formatted_rgb = ",".join(
                [str(value) for value in to_rgb]
            )  # é necessário juntar os valores para poder entregar no formato 'rgb()' para renderização no HTML
            rgb_list.append(f"rgb({formatted_rgb})")

        # spectral data gathering
        if spectral_start != -1:
            if start_index != 0:
                data_content = [
                    line.split("\t")[start_index + 1 :] for line in data_content
                ]
                spectral_start = spectral_start - start_index - 1
                spectral_end = spectral_end - start_index
                nm_index = nm_index - start_index - 1
            else:
                data_content = [line.split("\t")[start_index:] for line in data_content]
                spectral_start = spectral_start - start_index
                spectral_end = spectral_end - start_index + 1
                nm_index = nm_index - start_index

            # Second, removes all spaces, double spaces, tabular etc and replaces it with single space
            for row_index, row in enumerate(data_content):
                for col_index, col_value in enumerate(row):
                    data_content[row_index][col_index] = re.sub(
                        r"^\S\n\t+", "", col_value.strip()
                    )

            # Third, separates elements in the list that are not separated yet (specially spectral data from the -1 element in some cases)
            new_data = []
            for i in range(len(data_content)):
                split_values = [
                    value for element in data_content[i] for value in element.split()
                ]
                new_data.append(split_values)

            # DATA ORGANIZATION
            # Substituing eventual comma for dot in each element
            for index, line in enumerate(new_data):
                # Substituir vírgulas por pontos em cada elemento da linha
                new_data[index] = [value.replace(",", ".") for value in line]

                # Substituir aspas duplas no nome da amostra
                sample_name_list[index] = sample_name_list[index].replace('"', "")

                # Se o índice do nome não foi encontrado, concatenar todos os números até o primeiro "nm"
                if name_index == -1:
                    sample_name_list[index] = "-".join(line[start_index:nm_index])

            # Filling the start and end with (I can also use has_380 and no730 as conditionals for filling the empty elements)
            spectral_number = []
            for line in new_data:
                number = line[spectral_start:spectral_end]
                if not has_380:
                    number.insert(0, "0.000")
                    number.insert(0, "0.000")
                    number.append("0.000")
                    number.append("0.000")
                    number.append("0.000")

                spectral_number.append(number)
        else:
            spectral_number = []

        return {
            "header values": header_values,
            "start": cmyk_start,
            "end": cmyk_end,
            "has_lab": has_lab,
            "start_index": start_index,
            "sample_id_list": sample_id_list,
            "sample_name_list": sample_name_list,
            "cmyk_data_list": cmyk_data_list,
            "lab": lab,
            "reference_name_list": reference_name_list,
            "rgb": rgb_list,
            "descriptor": descriptor,
            "spectral_number": spectral_number,
        }


class ChartProofProcessingServices:
    """
    Analisa os inputs para processamento de dados do tipo FOGRA39
    """

    def data_filtering(self, uploaded_file):
        """
        Processamento do input
        """
        # header indexes variables
        header_start_index = None
        header_end_index = None
        header_values = None

        # cmyk and lab indexes variables
        cmyk_start = -1
        cmyk_end = -1
        lab_start = -1
        lab_end = -1

        # data indexes variables
        data_start_index = None
        data_end_index = None
        number_of_sets = None

        # Sample Id and Sample Name indexes
        id_index = -1
        name_index = -1
        has_name = False

        # Name of the input
        descriptor = ""

        # Boolean variables
        has_380 = False
        unkown_data = True

        is_nm = False

        for i, line in enumerate(uploaded_file):
            if "DESCRIPTOR" in line:
                descriptor = re.sub(r"^\S\n\t+", "", line.strip()).split()
            if line.strip() == "BEGIN_DATA_FORMAT":
                unkown_data = False
                header_start_index = i
            elif line.strip() == "END_DATA_FORMAT":
                header_end_index = i

            if line.strip() == "BEGIN_DATA":
                data_start_index = i
            elif line.strip() == "END_DATA":
                data_end_index = i

            if "NUMBER_OF_SETS" in line.strip():
                line = re.sub(r"^\S\n\t+", "", line.strip()).split()
                number_of_sets = int(line[1])

        # Error
        if unkown_data:
            return "Unknown data format"

        # HEADER FILTERING
        if header_start_index is not None and header_end_index is not None:
            header_line = uploaded_file[header_start_index + 1 : header_end_index]

        # Error if CMYK string is not included in the header
        if not any("CMYK" in line for line in header_line):
            return "No CMYK data found"

        # Searches for LAB values
        has_lab = bool(any("LAB" in line for line in header_line))

        header_values = re.sub(r"(?<=\S)\s+(?=\S)", "\t", header_line[0]).split("\t")
        if not header_values[-1]:
            header_values = header_values[:-1]

        for index, value in enumerate(header_values):
            # busca dado espectral
            if "380" in value:
                spectral_start = index
                has_380 = True
            elif "400" in value and not has_380:
                spectral_start = index
            if "700" in value:
                spectral_end = index
            elif "730" in value and has_380:
                no_730 = False
                spectral_end = index

            if "CMYK_C" in value:
                cmyk_start = index
            elif "CMYK_K" in value:
                cmyk_end = index

            if has_lab and "LAB_L" in value:
                lab_start = index
            elif has_lab and "LAB_B" in value:
                lab_end = index

            if re.search(r"id", value, re.IGNORECASE):
                id_index = index
            if re.search(r"name", value, re.IGNORECASE):
                name_index = index
                has_name = True

        # DATA FILTERING
        if data_start_index is not None and data_start_index is not None:
            data_content = uploaded_file[data_start_index + 1 : data_end_index]

        # Error
        if number_of_sets != len(data_content):
            return "Number of sets is not the same as the number of colors!"

        # Calculate the effective starting index for data_content
        if id_index != -1 and name_index != -1:
            start_index = max(id_index, name_index)
        elif id_index != -1:
            start_index = id_index
        elif name_index != -1:
            start_index = name_index
        else:
            # Both id_index and name_index are -1, start from the beginning
            start_index = 0

        sample_id_list = []
        sample_name_list = []
        cmyk_data_list = []
        reference_name_list = []
        lab = []
        rgb_list = []
        for index, line in enumerate(data_content):
            line = re.sub(r"(?<=\S)\s+(?=\S)", "\t", line.strip()).split("\t")
            sample_id = line[id_index] if id_index != -1 else index + 1
            sample_id_list.append(sample_id)

            if has_name:
                sample_name = line[name_index] if name_index != -1 else ""
                sample_name_list.append(sample_name)

            # getting CMYK data
            cmyk_data = line[cmyk_start : cmyk_end + 1]
            cmyk_data_list.append(cmyk_data)

            # getting the reference_name, AKA, 000-000-1000
            reference_name = get_reference_name(cmyk_data)
            reference_name_list.append(reference_name)

            if lab_start != 1:
                lab_data = line[lab_start : lab_end + 1]
                lab = lab_data

            # converting to RGB
            # to_rgb = cmyk_to_rgb(cmyk_data)
            to_rgb = lab_to_rgb(lab)
            formatted_rgb = ",".join(
                [str(value) for value in to_rgb]
            )  # é necessário juntar os valores para poder entregar no formato 'rgb()' para renderização no HTML
            rgb_list.append(f"rgb({formatted_rgb})")

        # spectral data gathering
        if start_index != 0:
            data_content = [
                line.split("\t")[start_index + 1 :] for line in data_content
            ]
            spectral_start = spectral_start - start_index - 1
            spectral_end = spectral_end - start_index
            nm_index = nm_index - start_index - 1
        else:
            data_content = [line.split("\t")[start_index:] for line in data_content]
            spectral_start = spectral_start - start_index
            spectral_end = spectral_end - start_index + 1
            nm_index = nm_index - start_index

        # Second, removes all spaces, double spaces, tabular etc and replaces it with single space
        for row_index, row in enumerate(data_content):
            for col_index, col_value in enumerate(row):
                data_content[row_index][col_index] = re.sub(
                    r"^\S\n\t+", "", col_value.strip()
                )

        # Third, separates elements in the list that are not separated yet (specially spectral data from the -1 element in some cases)
        new_data = []
        for i in range(len(data_content)):
            split_values = [
                value for element in data_content[i] for value in element.split()
            ]
            new_data.append(split_values)

        # DATA ORGANIZATION
        # Substituing eventual comma for dot in each element
        for index, line in enumerate(new_data):
            # Substituir vírgulas por pontos em cada elemento da linha
            new_data[index] = [value.replace(",", ".") for value in line]

            # Substituir aspas duplas no nome da amostra
            sample_name_list[index] = sample_name_list[index].replace('"', "")

            # Se o índice do nome não foi encontrado, concatenar todos os números até o primeiro "nm"
            if name_index == -1:
                sample_name_list[index] = "-".join(line[start_index:nm_index])

        # Filling the start and end with (I can also use has_380 and no730 as conditionals for filling the empty elements)
        spectral_number = []
        for line in new_data:
            number = line[spectral_start:spectral_end]
            if not has_380:
                number.insert(0, "0.000")
                number.insert(0, "0.000")
                number.append("0.000")
                number.append("0.000")
                number.append("0.000")

            spectral_number.append(number)

        return {
            "header values": header_values,
            "start": cmyk_start,
            "end": cmyk_end,
            "has_lab": has_lab,
            "start_index": start_index,
            "sample_id_list": sample_id_list,
            "sample_name_list": sample_name_list,
            "cmyk_data_list": cmyk_data_list,
            "lab": lab,
            "reference_name_list": reference_name_list,
            "rgb": rgb_list,
            "descriptor": descriptor,
            "spectral_number": spectral_number,
        }


# Definindo uma função para formatar os valores
def get_reference_name(valores):
    """
    Creates the reference name, ex: 100-000-000-000
    """
    formatted_values = []
    for valor in valores:
        # Verificar se o valor contém ponto decimal
        if "." in valor:
            # Se contém, remover os zeros após o ponto e formatar como porcentagem
            formatted_value = "-".join(
                [f"{int(float(v.strip())):03d}" for v in valor.split(",")]
            )
        else:
            # Se não contém, formatar como número inteiro
            formatted_value = "-".join(
                [f"{int(v.strip()):03d}" for v in valor.split(",")]
            )
        formatted_values.append(formatted_value)
    return "-".join(formatted_values)


def cmyk_to_rgb(data):
    """
    Convert CMYK to RGB
    """

    # para casos 100.00 ou 100, respectivamente
    to_number = [
        float(value) / 100 if "." in value else int(value) / 100 for value in data
    ]
    to_cmy = colour.CMYK_to_CMY(to_number)
    to_rgb = colour.CMY_to_RGB(to_cmy)
    to_rgb_255 = [round(value * 255) for value in to_rgb]
    return to_rgb_255


def lab_to_rgb(data):
    """
    Convert LAB to RGB
    """

    # Crie um objeto LabColor
    lab_color = LabColor(*data)

    # Converta para sRGBColor
    rgb_color = convert_color(lab_color, sRGBColor)

    # Obtenha os valores RGB
    r = int(rgb_color.rgb_r * 255)
    g = int(rgb_color.rgb_g * 255)
    b = int(rgb_color.rgb_b * 255)

    return [r, g, b]


def correct_lab_format(lab_values):
    """
    Substitui vírgula por ponto, caso tenha

    """
    new_values = []
    for lab_value in lab_values:
        if "," in lab_value:
            corrected = lab_value.replace(",", ".")
            new_values.append(corrected)
        else:
            new_values.append(lab_value)

    return new_values


"""
chart cyan - 0, 151, 218
sample cyan - 0, 153, 216

"""
