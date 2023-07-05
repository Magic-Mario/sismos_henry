import requests
import pandas as pd
from pymongo import MongoClient, UpdateOne
from pymongo.server_api import ServerApi
import time
import sys
import os
from datetime import timedelta



# definición de constantes
#clave para acceder a mongo
password = os.getenv("MONGODB_PASSWORD")
print(password)

# se establece el tiempo de la última consulta para iniciar el programa
last_query_time = "2018-01-01"

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

# se establece la url y los parámetros de la request
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
params = {"format": "geojson", "starttime": "2014-01-01", "endtime": "2014-01-31"}

# máximo de registros que la API de USGS devolverá por consulta
LIMIT = 20000

#### funciones del programa

#función para búsqueda de país dentro de las propiedades de la respuesta de la API
def find_country(place):
    # busca en la lista de paises
    for pais in paises:
        if pais.lower() in place.lower():
            return pais.lower()
    return next(
        ("usa" for estado in us_estados if estado.lower() in place.lower()),
        "other",
    )

def main():
    global last_query_time

    while True:
        try:
            # establece el tiempo de inicio en el tiempo de la última consulta
            params["starttime"] = last_query_time

            # calcula el tiempo final como la hora actual
            endtime = pd.Timestamp.now()

            # establece un contador para llevar la cuenta de cuántos registros se han obtenido
            count = 0

            while True:
                # configura el parámetro de finalización para ser una hora después del tiempo de inicio
                params["endtime"] = (pd.Timestamp(params["starttime"]) + timedelta(hours=1)).isoformat()

                if pd.Timestamp(params["endtime"]) > endtime:
                    params["endtime"] = endtime.isoformat()

                # llama a la API
                response = requests.get(url, params=params)
                response.raise_for_status()

                # Procesa los datos de la API
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
                        if place and location.lower() in place.lower():
                            filtered_features.append(feature)
                            break  # se termina la busqueda buscar en los otros lugares una vez que encontramos una coincidencia

                # Ahora 'filtered_features' contiene solo los terremotos que ocurrieron en los países y estados especificados

                # Crear una lista vacía para almacenar los datos
                data_list = []

                for feature in filtered_features:
                    # Extraer información de properties y geometry
                    properties = feature["properties"]
                    geometry = feature["geometry"]

                    # Crear un diccionario con los datos que necesitamos
                    data_dict = {
                        "id": f"{geometry['coordinates'][0]}_{geometry['coordinates'][1]}_{properties['mag']}_{properties['time']}", #id sintetica
                        "place": properties["place"],
                        "mag": properties["mag"],
                        "time": pd.to_datetime(properties["time"], unit="ms"),  # convertir el tiempo a formato legible
                        "lon": geometry["coordinates"][0],
                        "lat": geometry["coordinates"][1],
                        "depth": geometry["coordinates"][2],
                    }

                    # Añadir el diccionario a la lista
                    data_list.append(data_dict)

                # Crear un DataFrame a partir de la lista de diccionarios
                df = pd.DataFrame(data_list)

                # se crea la columna con la denominación de cada país según la columna place
                df["country"] = df["place"].apply(find_country)
                
                print(df)

                try:
                    # se conecta a MongoDB
                    uri = f"mongodb+srv://picassojuanpablo:{password}@cluster0.zet6ttc.mongodb.net/?retryWrites=true&w=majority"

                    # Create a new client and connect to the server
                    client = MongoClient(uri, server_api=ServerApi('1'))
                    
                    #print(client)
                    db = client["pf-henry"]
                    collection = db["api_usgs"]

                    # se convierte el DataFrame en una lista de diccionarios para que se pueda almacenar en MongoDB
                    data_dict = df.to_dict("records")

                    # Crear una lista de operaciones UpdateOne
                    operations = [
                        UpdateOne({"id": record["id"]}, {"$set": record}, upsert=True) for record in data_dict
                    ]

                    # Ejecutar las operaciones con bulk_write
                    collection.bulk_write(operations)
                    

                except Exception as e:
                    print(f"Error al conectarse a MongoDB: {e}", file=sys.stderr)
                    
                # actualiza el contador con el número de registros obtenidos
                count += len(response.json()["features"])

                # si el número total de registros es inferior al límite, entonces se han obtenido todos los registros
                # para este intervalo de tiempo y se puede pasar al siguiente intervalo de tiempo
                if count < LIMIT:
                    break

                # si se han obtenido el máximo número de registros, actualiza el tiempo de inicio y repite el ciclo
                params["starttime"] = params["endtime"]

        # actualiza el tiempo de la última consulta para la próxima vez
            last_query_time = params["endtime"]
            print(last_query_time)

        except Exception as e:
            print(f"Error al llamar a la API: {e}", file=sys.stderr)

        # Espera una hora antes de la próxima iteración
        # time.sleep(3600)
        time.sleep(100)


if __name__ == "__main__":
    main()
