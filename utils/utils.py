# STANDARD IMPORTS
import itertools
import re
from datetime import date
from datetime import datetime
import pytz
from django.core.mail import EmailMessage

import pandas as pd

def return_categories(app, type):
    
    properties = PropertiesServices.get_charts(app, type) # type: ignore
    properties = pd.DataFrame(properties)

    list_categories = properties['categories'].drop_duplicates().values.tolist()

    return list_categories




def add_dynamic_filters(dynamic_filters, dict):

    _mutable = dynamic_filters._mutable

    # set to mutable
    dynamic_filters._mutable = True

    for key, value in dict.items():
        try:
            dynamic_filters[key]=value
        except:
            pass

    dynamic_filters._mutable = _mutable
    
    return dynamic_filters

def pop_dynamic_filters(dynamic_filters, columns):

    _mutable = dynamic_filters._mutable

    # set to mutable
    dynamic_filters._mutable = True

    for column in columns:
        try:
            dynamic_filters.pop(column)
        except:
            pass

    dynamic_filters._mutable = _mutable
    
    return dynamic_filters


def send_email(data):

    email = EmailMessage(subject=data['email_subject'], body=data['email_body'], from_email='tech@saltrh.com.br', to=[data['email']])
    result = email.send()
    return result


def get_time_timezone():
    timeZ_Af = pytz.timezone('Africa/Mogadishu')
    dt_Af = datetime.now(timeZ_Af)
    utc_Af = dt_Af.astimezone(timeZ_Af)

    return utc_Af


def sort_dataframe_by_category(df, column):
    # spliting each first number from each row
    new = df[column].str.split(". ", n=1, expand=True)

    # adding to columns
    df["Order"] = new[0]
    df["Categoria"] = new[1]

    # sorting categories in ascending
    try:
        df["Order"] = df["Order"].astype('int32')
    except:
        pass
    
    df = df.sort_values(["Order"])

    # dropping table categoria_4
    # df.drop(columns=[column, "Order"], inplace=True)
    # df = df.rename(columns={'Categoria': column})

    return df


def get_selected_year_values(series: list, years_list: list) -> dict:
    selected_values = {}

    years_list = [int(year) for year in years_list]
    max_year = max(years_list)
    
    for serie in series:
        selected = serie.get("name")

        year = (re.findall('\d+', selected)).pop()

        if int(year) == max_year:
            selected_values[selected] = True

        else:
            selected_values[selected] = False

    return selected_values


def define_cor(cor):
    if cor <= 35:
        return '#19D7AA'
    elif (cor >= 35) & (cor < 50):
        return '#CEC6CE'
    else:
        return '#EF647C'


def drill_down(dynamic_filters, properties, columns, titles, drill_down_level, filtro_categoria):
    filters_dict = dict(dynamic_filters)

    drill_down_level = 'drill_down_{}'.format(drill_down_level)

    try:
        drill_down_field = filters_dict['drill_down_field'][0]
        drill_down = properties['drill_down'].drop_duplicates().values.tolist()

        drill_down_item = drill_down[titles.index(drill_down_field)]
        column_drill_down = columns[titles.index(drill_down_item)]
        column_drill_down_field = columns[titles.index(drill_down_field)]

        new_columns = []

        for column in columns:

            if column == column_drill_down_field:
                new_columns.append(column_drill_down)

            elif column == column_drill_down:

                continue
            else:
                new_columns.append(column)

        return new_columns

    except:
        teste = None

    return columns


def deleta_campo(filters, campos):
    for campo in campos:

        try:
            del filters[campo]
        except:
            campos = campo

    return filters


def valida_campo(dynamic_filters, campo):
    try:
        return dynamic_filters[campo][0]
    except:
        campos = campo


def ajusta_no_mes(meses):
    meses = [mes.split('-')[1] for mes in meses]

    map_dictionary_month = {
        '01': 'Jan',
        '02': 'Feb',
        '03': 'Mar',
        '04': 'Apr',
        '05': 'May',
        '06': 'Jun',
        '07': 'Jul',
        '08': 'Aug',
        '09': 'Sep',
        '10': 'Oct',
        '11': 'Nov',
        '12': 'Dec'
    }

    map_response = [map_dictionary_month[mes] for mes in meses]

    return map_response


def format_data_mes_ano(dates: str, months: str) -> list:
    format_date = []

    for (date, month) in itertools.zip_longest(dates, months):
        year = date[0:4]
        raw_date = month + "/" + year
        format_date.append(raw_date)

    return format_date


def get_color_order_for_voluntary_and_involuntary(chart):
    category_turnover = []
    for category in chart["series"]["series"]:
        cat = category.get("name")
        category_turnover.append(cat)

    if category_turnover[0] == "Voluntary" or category_turnover[0] == "Voluntário":
        chart.update({'color': ["#2896DC", "#19D7AA"]})
    if category_turnover[0] == "Involuntary" or category_turnover[0] == "Involuntário":
        chart.update({'color': ["#19D7AA", "#2896DC"]})

    return chart


def formata_mes(meses):
    meses = [str(mes.split('-')[1]) for mes in meses]

    map_dictionary_month = {
        '01': '01/2022',
        '02': '02/2022',
        '03': '03/2022',
        '04': '04/2022',
        '05': '05/2022',
        '06': '06/2022',
        '07': '07/2022',
        '08': '08/2022',
        '09': '09/2022',
        '10': '10/2022',
        '11': '11/2022',
        '12': '12/2022'
    }

    map_response = [map_dictionary_month[ano_mes] for ano_mes in meses]

    return map_response