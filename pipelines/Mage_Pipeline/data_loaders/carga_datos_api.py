import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import io
import pandas as pd
import requests
import pytz

# Obtener la contraseña de MongoDB de una variable de entorno
password = os.getenv("MONGODB_PASSWORD")

# Establecer la URL de conexión a MongoDB
uri = f"mongodb+srv://copito:golazo@cluster1.krfn9qj.mongodb.net/?retryWrites=true&w=majority"

# Crear un cliente de MongoDB y establecer la versión de la API del servidor
client = MongoClient(uri, server_api=ServerApi('1'))

# Seleccionar la base de datos y la colección correspondientes
db = client["Sismos"]
collection = db["prueba"]

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query?"
    limit = 10000  # Número máximo de terremotos a obtener

    # Recuperar los IDs existentes en la base de datos
    existing_ids = set(collection.distinct("ID"))

    data_list = []

    # Recuperar el último tiempo de consulta de la colección "metadata"
    metadata = collection.find_one({"name": "last_query_time"})
    if metadata is not None:
        last_query_time = metadata["value"]
    else:
        # En caso de que no exista la metadata en la base de datos, se establece el valor inicial
        last_query_time = "2018-06-15"

    start_date = last_query_time  # Utilizar el último tiempo de consulta como inicio de la nueva consulta
    end_date = "2023-07-30"
    params = {
        "format": "geojson",
        "starttime": start_date,
        "endtime": end_date,
        "orderby": "time",  # Ordenar los terremotos por tiempo, de más reciente a más antiguo
        "limit": limit  # Limitar el número de terremotos a obtener
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()

        for feature in data["features"]:
            properties = feature["properties"]
            magnitude = properties["mag"]
            place = properties["place"]
            date_time = pd.to_datetime(properties["time"], unit='ms')
            date_time = date_time.tz_localize(pytz.UTC)
            date_time = date_time.astimezone(pytz.timezone('America/New_York'))
            mag_type = properties["magType"]
            event_type = properties["type"]
            latitude = feature["geometry"]["coordinates"][1]
            longitude = feature["geometry"]["coordinates"][0]
            depth = feature["geometry"]["coordinates"][2]
            event_id = feature["id"]

            if event_id not in existing_ids:  # Filtrar los registros que ya existen en la base de datos
                data_list.append([magnitude, place, date_time.strftime("%Y-%m-%d %H:%M:%S"), mag_type, event_type, latitude, longitude, depth, event_id])

    else:
        print("Error en la solicitud:", response.status_code)

    df = pd.DataFrame(data_list, columns=["Magnitud", "Lugar", "Fecha", "Tipo de Magnitud", "Tipo de Evento", "Latitud", "Longitud", "Profundidad", "ID"])

    # Actualizar el último tiempo de consulta en la colección "metadata" solo si se cargaron nuevos terremotos
    if not df.empty:
        last_query_time = df["Fecha"].max()  # Obtener la fecha más reciente de los terremotos cargados
        collection.update_one({"name": "last_query_time"}, {"$set": {"value": last_query_time}}, upsert=True)

    return df
