# sourcery skip: assign-if-exp
import requests
import pandas as pd
from pymongo import MongoClient, UpdateOne
from pymongo.server_api import ServerApi
import time
import sys
import os
from datetime import timedelta
import re  # importar el módulo re para trabajar con expresiones regulares



# definición de constantes
#clave para acceder a mongo
password = os.getenv("MONGODB_PASSWORD")
#print(password)

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

us_state_abbreviations = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
                          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


# se establece la url y los parámetros de la request
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
params = {"format": "geojson", "starttime": "2014-01-01", "endtime": "2014-01-31"}

# máximo de registros que la API de USGS devolverá por consulta
LIMIT = 20000

# Crear un nuevo cliente y conectarse al servidor
uri = f"mongodb+srv://picassojp:{password}@cluster0.cchanol.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["pf-henry"]
collection = db["db-pf-henry"]
collection_meta = db["metadata"]

# Recuperar last_query_time de MongoDB al inicio del programa
metadata = collection_meta.find_one({"name": "last_query_time"})
if metadata is not None:
    last_query_time = metadata["value"]
else:
    # En caso de que no exista la metadata en la base de datos, se establece el valor inicial
    last_query_time = pd.Timestamp.now().isoformat()

#variable para pruebas
# last_query_time = "2016-01-01"

#### funciones del programa

#función para búsqueda de país dentro de las propiedades de la respuesta de la API
def find_country(place):
    # busca en la lista de paises
    for pais in paises:
        if pais.lower() in place.lower():
            return pais.lower()
    return "usa"

def main():
    global last_query_time

    while True:
        try:
            # establece el tiempo de inicio en el tiempo de la última consulta
            params["starttime"] = last_query_time
            
            #print(last_query_time)

            # calcula el tiempo final como la hora actual
            endtime = pd.Timestamp.now()

            # configura el parámetro de finalización para ser una hora después del tiempo de inicio
            params["endtime"] = (pd.Timestamp(params["starttime"]) + timedelta(hours=1)).isoformat()

            if pd.Timestamp(params["endtime"]) > endtime:
                params["endtime"] = endtime.isoformat()
                
            #print(params["endtime"])

            # llama a la API
            response = requests.get(url, params=params)
            response.raise_for_status()

            # Procesa los datos de la API
            # se guardan los datos de la consulta a la API
            data = response.json()
            
            # se toman los datos del diccionario correspondiente
            features = data["features"]
            
            #print(features)

            filtered_features = []

            #iteración sobre todos los registros que trajo la consulta
            for feature in features:
                if 'place' in feature['properties']:
                    place = feature['properties']['place']
                else:
                    place = None
                    #print('asigno none a place')
                for location in (paises + us_estados):  # se verifica tanto en países como en estados de EE.UU.
                    if place and location.lower() in place.lower():
                        filtered_features.append(feature)
                        break  # se termina la busqueda buscar en los otros lugares una vez que encontramos una coincidencia
                    # buscar la ubicación en los bordes del texto o rodeada por caracteres no alfanuméricos 
                for location in us_state_abbreviations:
                    #print('busca por abreviatura')
                    pattern = r', ' + re.escape(location.lower()) + r'\b' #se buscan las abreviaturas con una coma previa
                    #print(pattern)
                    if place and re.search(pattern, place.lower()):
                        filtered_features.append(feature)
                        break  # se termina la busqueda en los otros lugares una vez que encontramos una coincidencia

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
                    "time0": properties["time"],  # convertir el tiempo a formato legible
                    "lon": geometry["coordinates"][0],
                    "lat": geometry["coordinates"][1],
                    "depth": geometry["coordinates"][2],
                }

                # Añadir el diccionario a la lista
                data_list.append(data_dict)

            # Crear un DataFrame a partir de la lista de diccionarios
            df = pd.DataFrame(data_list)
            #print(df)
            
            # Verificar si el DataFrame es vacío
            if not df.empty:
                # Se crea la columna con la denominación de cada país según la columna place
                df["country"] = df["place"].apply(find_country)

                #print(df)

                try:
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
                    
                # se actualiza el tiempo de inicio y repite el ciclo
                #params["starttime"] = params["endtime"]
            
            else:
                print("No se encontraron terremotos en las ubicaciones especificadas durante este intervalo de tiempo.")
                # se actualiza el tiempo de inicio y repite el ciclo
                #params["starttime"] = params["endtime"]

            # actualiza el tiempo de la última consulta para la próxima vez
            last_query_time = params["endtime"]
            #print(last_query_time)
            
            # Al final de cada ciclo de consulta, guardar last_query_time en MongoDB
            collection_meta.update_one({"name": "last_query_time"}, {"$set": {"value": last_query_time}}, upsert=True)

        except Exception as e:
            print(f"Error al llamar a la API: {e}", file=sys.stderr)

        # Espera los segundos establecidos antes de la próxima iteración
        # time.sleep(3600)
        time.sleep(15)


if __name__ == "__main__":
    main()
