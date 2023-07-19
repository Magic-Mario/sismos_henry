import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json


def fetch_earthquake_data(start_date, end_date):
    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={start_date}&endtime={end_date}"
    return pd.read_csv(url)


# sourcery skip: use-itertools-product
start_year = 2013
end_year = 2014

for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-31"

        data = fetch_earthquake_data(start_date, end_date)

        # Aquí puedes realizar las operaciones o análisis que necesites con los datos obtenidos
        df = pd.DataFrame(data)


base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query?"
start_year = 2018
end_year = 2023

data_list = []

for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-31"
        params = {
            "format": "geojson",
            "starttime": start_date,
            "endtime": end_date,
            "limit": 20000,  # Limitamos la cantidad de eventos por solicitud
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()

            for feature in data["features"]:
                properties = feature["properties"]
                magnitude = properties["mag"]
                place = properties["place"]
                date_time = pd.to_datetime(properties["time"], unit="ms")
                mag_type = properties["magType"]
                event_type = properties["type"]
                latitude = feature["geometry"]["coordinates"][1]
                longitude = feature["geometry"]["coordinates"][0]
                depth = feature["geometry"]["coordinates"][2]
                event_id = feature["id"]

                data_list.append(
                    [
                        magnitude,
                        place,
                        date_time,
                        mag_type,
                        event_type,
                        latitude,
                        longitude,
                        depth,
                        event_id,
                    ]
                )
        else:
            print("Error en la solicitud:", response.status_code)

df = pd.DataFrame(
    data_list,
    columns=[
        "Magnitud",
        "Lugar",
        "Fecha",
        "Tipo de Magnitud",
        "Tipo de Evento",
        "Latitud",
        "Longitud",
        "Profundidad",
        "ID",
    ],
)


df_copia = df.copy()

# los paises y los estados (USA) que se buscan filtrar
chile = ["Chile"]
japon = ["Japan"]
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

# Reemplazar valores NaN con cadena vacía
df_copia["Lugar"] = df_copia["Lugar"].fillna("")

# Filtrar por países y estados
df_chile = df_copia[df_copia["Lugar"].str.contains("|".join(chile))]
df_japan = df_copia[df_copia["Lugar"].str.contains("|".join(japon))]
df_usa = df_copia[df_copia["Lugar"].str.contains("|".join(us_estados))]


def limpiar_lugar(lugar):
    if "of" in lugar:
        lugar = lugar.split("of")[1].strip()
    return lugar


df_copia_chile = df_chile.copy()

df_copia_chile["Lugar"] = df_copia_chile["Lugar"].apply(limpiar_lugar)


# Extraer solo las ciudades de la columna 'Lugar'
df_copia_chile["Ciudad"] = df_copia_chile["Lugar"].apply(lambda x: x.split(", ")[0])

# Eliminar la columna 'Lugar'
df_copia_chile.drop("Lugar", axis=1, inplace=True)


# Agregar una nueva columna 'País' con el valor 'Chile'
df_copia_chile["País"] = "Chile"

# Crear una lista con el nuevo orden de columnas
new_columns_order = [
    "País",
    "Ciudad",
    "Magnitud",
    "Fecha",
    "Tipo de Magnitud",
    "Tipo de Evento",
    "Latitud",
    "Longitud",
    "Profundidad",
    "ID",
]

# Reordenar las columnas en el DataFrame
df_copia_chile = df_copia_chile[new_columns_order]


import missingno as msno

msno.matrix(df_copia_chile)


df_copia_japan = df_japan.copy()


# Crear una función para limpiar la columna 'Lugar' en el caso de Japón
def limpiar_lugar_japon(lugar):
    if " of " in lugar:
        lugar = lugar.split(" of ")[1].split(",")[0].strip()
    elif ", Japan" in lugar:
        lugar = lugar.replace(", Japan", "")
    return lugar


# Aplicar la función de limpieza a la columna 'Lugar' en el DataFrame de Japón
df_copia_japan["Lugar"] = df_copia_japan["Lugar"].apply(limpiar_lugar_japon)


# Cambiar el nombre de la columna 'Lugar' a 'Ciudad'
df_copia_japan.rename(columns={"Lugar": "Ciudad"}, inplace=True)

# Agregar una nueva columna 'País' con el valor 'Japón'
df_copia_japan["País"] = "Japón"

# Crear una lista con el nuevo orden de columnas
new_columns_order = [
    "País",
    "Ciudad",
    "Magnitud",
    "Fecha",
    "Tipo de Magnitud",
    "Tipo de Evento",
    "Latitud",
    "Longitud",
    "Profundidad",
    "ID",
]

# Reordenar las columnas en el DataFrame
df_copia_japan = df_copia_japan[new_columns_order]


msno.matrix(df_copia_japan)


df_copia_usa = df_usa.copy()


# Crear una función para extraer el estado de Estados Unidos del lugar
def extraer_estado(lugar):
    estados = [
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

    return next((estado for estado in estados if estado in lugar), lugar)


# Aplicar la función para extraer el estado a la columna 'Lugar' en el DataFrame de Estados Unidos
df_copia_usa["Lugar"] = df_copia_usa["Lugar"].apply(extraer_estado)


# Cambiar el nombre de la columna 'Lugar' a 'Ciudad'
df_copia_usa.rename(columns={"Lugar": "Ciudad"}, inplace=True)

# Agregar una nueva columna 'País' con el valor 'Estados Unidos'
df_copia_usa["País"] = "Estados Unidos"

# Crear una lista con el nuevo orden de columnas
new_columns_order = [
    "País",
    "Ciudad",
    "Magnitud",
    "Fecha",
    "Tipo de Magnitud",
    "Tipo de Evento",
    "Latitud",
    "Longitud",
    "Profundidad",
    "ID",
]

# Reordenar las columnas en el DataFrame
df_copia_usa = df_copia_usa[new_columns_order]

msno.matrix(df_copia_usa)

# Concatenar los DataFrames
df_combined = pd.concat([df_copia_usa, df_copia_japan, df_copia_chile])

# Reiniciar los índices del DataFrame resultante
df_combined = df_combined.reset_index(drop=True)


unique_event_types = df_combined["Tipo de Evento"].unique()
print("Valores únicos en 'Tipo de Evento':")
print(unique_event_types)

df_earthquakes = df_combined[df_combined["Tipo de Evento"] == "earthquake"]
