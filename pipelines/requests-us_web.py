#!/usr/bin/env python
# coding: utf-8

# # 1. Extracción de datos de la API de USGS

import requests
import pandas as pd


# los paises y los estados (USA) que se buscan filtrar
paises = ["Chile", "Japan"]
us_estados = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
]


def find_country(place):
    # busca en la lista de paises
    for pais in paises:
        if pais.lower() in place.lower():
            return pais.lower()
    return next(
        ("usa" for estado in us_estados if estado.lower() in place.lower()),
        "other",
    )


# se establece la url y los parámetros de la request
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
params = {"format": "geojson", "starttime": "2014-01-01", "endtime": "2014-01-31"}
response = requests.get(url, params=params)

# se guardan los datos de la consulta a la API
data = response.json()


# se toman los datos del diccionario correspondiente
features = data["features"]


filtered_features = []

for feature in features:
    place = feature["properties"]["place"]
    for location in (
        paises + us_estados
    ):  # se verifica tanto en países como en estados de EE.UU.
        if location.lower() in place.lower():
            filtered_features.append(feature)
            break  # se termina la busqueda buscar en los otros lugares una vez que encontramos una coincidencia

# Ahora 'filtered_features' contiene solo los terremotos que ocurrieron en los países y estados especificados


len(filtered_features)  # se revisa la cantidad de registros filtrados


# Crear una lista vacía para almacenar los datos
data_list = []

for feature in filtered_features:
    # Extraer información de properties y geometry
    properties = feature["properties"]
    geometry = feature["geometry"]

    # Crear un diccionario con los datos que necesitamos
    data_dict = {
        "place": properties["place"],
        "mag": properties["mag"],
        "time": pd.to_datetime(
            properties["time"], unit="ms"
        ),  # convertir el tiempo a formato legible
        "lon": geometry["coordinates"][0],
        "lat": geometry["coordinates"][1],
        "depth": geometry["coordinates"][2],
    }

    # Añadir el diccionario a la lista
    data_list.append(data_dict)

# Crear un DataFrame a partir de la lista de diccionarios
df = pd.DataFrame(data_list)


df.shape  # dimensiones del df


# se crea la columna con la denominación de cada país según la columna place
df["country"] = df["place"].apply(find_country)


df.head()
