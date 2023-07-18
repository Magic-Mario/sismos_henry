from fastapi import FastAPI, Path, Query, HTTPException
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from dateutil import parser
import os
from pydantic import BaseModel
import pickle
from typing import List, Optional
import numpy as np


description = """
Este sistema permite realizar diversas consultas sobre sismos registrados en Estados Unidos, Japón y Chile 
desde el año 2016 hasta la actualidad 🚀
"""

app = FastAPI(
    title="Sistema de Información de Sismos",
    description=description,
    version="0.0.1",
    contact={
        "name": "Juan Pablo Picasso",
        "GitHub": "https://github.com/picassojp",
        "email": "picassojuanpablo@gmail.com",
    },
)

password = os.environ["MONGODB_PASSWORD"]


# datos para acceder a la base de datos
uri = f"mongodb+srv://picassojp:{password}@cluster0.cchanol.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi("1"))

db = client["pf-henry"]  # base de datos
collection = db["db-pf-henry"]  # colección
user_collection = db["users"]  # colección 'users' del bot


# Cargar el modelo
with open("classf_model.pkl", "rb") as f:
    model = pickle.load(f)


class User(BaseModel):
    id_chat: str
    country: str


@app.get("/date/")
async def get_quakes_by_date(start_date: str, end_date: str, limit: int = 10000):
    """
    Esta función devuelve una lista con los registros de sismos entre dos fechas especificadas (formato mm/dd/aa) con un límite predeterminado de 10000 registros.
    """

    try:
        start_date_obj = parser.parse(start_date)  # convierte la fecha al formato necesario para la request
        end_date_obj = parser.parse(end_date)
    except ValueError:  # manejo de error con el formato de la fecha
        raise HTTPException(status_code=400, detail="Fecha proporcionada en formato no válido. Por favor, proporciona una fecha válida.")

    quake_list = []

    for quake in collection.find(
        {"time": {"$gte": start_date_obj, "$lte": end_date_obj}}
    ).limit(limit):  # se filtran los documentos según los valores de fechas y se limita la cantidad de registros
        quake["_id"] = str(
            quake["_id"]
        )  # se modifica el formato del id de mongodb (bson)
        quake_list.append(quake)  # se apendean los documentos en una lista
    return quake_list


@app.get("/magnitude/{min_magnitude}/{max_magnitude}")
async def get_quakes_by_magnitude(
    min_magnitude: float = Path(0.0), max_magnitude: float = Path(10.0), limit: int = 10000):
    """
    Esta función devuelve todos los registros de sismos según una magnitud mínima (límite inferior 0.0) y una máxima (límite superior 10.0). De forma predeterminada estos valores corresponden a los límites de la escala (0-10)
    """
    quake_list = []
    for quake in collection.find(
        {"mag": {"$gte": min_magnitude, "$lte": max_magnitude}}
    ).limit(limit):  # se filtran los documentos según los valores de magnitud y se limita la cantidad de registros
        quake["_id"] = str(
            quake["_id"]
        )  # se modifica el formato del id de mongodb (bson)
        quake_list.append(quake)  # se apendean los documentos en una lista
    return quake_list


@app.get("/depth/{min_depth}/{max_depth}")
async def get_quakes_by_depth(
    min_depth: float = Path(0), max_depth: float = Path(1000), limit: int = 10000):
    """
    Esta función devuelve todos los registros de sismos según una profundidad mínima y una máxima expresada en kilómetros. De forma predeterminada estos valores corresponden a los límites típicos (0-1000)
    """
    quake_list = []
    for quake in collection.find(
        {"depth": {"$gte": min_depth, "$lte": max_depth}}
    ).limit(limit):  # se filtran los documentos según los valores de profundidad y se limita la cantidad de registros
        quake["_id"] = str(
            quake["_id"]
        )  # se modifica el formato del id de mongodb (bson)
        quake_list.append(quake)  # se apendean los documentos en una lista
    return quake_list


country_traduccion = {
    "estados unidos": "usa",
    "japon": "japan",
    "japón": "japan",
}  # un diccionario para traducir los nombres de los países

@app.get("/country/{country}")
async def get_quakes_by_country(country: str, latest: bool = False, limit: Optional[int] = None):
    """
    Esta función devuelve todos los registros de sismos según alguno de los tres países posibles: "usa", "japan" y "chile".
    Si latest es True, devuelve solo el registro más reciente.
    """
    country = country.lower()  # convierte el nombre del país a minúsculas
    
    if country in country_traduccion:
        country = country_traduccion[country]  # traduce el nombre del país si es necesario
    
    if latest:
        cursor = (
            collection.find(
                {"country": country},
                {"_id": 1, "id": 1, "mag": 1, "depth": 1, "time": 1, "place": 1},
            )
            .sort("time", -1)
            .limit(1))  # se usa la proyección de mongoDB para filtrar las variables de interés, se ordenan de forma decreciente y se limita la salida a 1
        try:
            quake = next(cursor)
            quake["_id"] = str(quake["_id"])
            return quake
        except (StopIteration):  # maneja la excepción de que la consulta no devuelva ningún registro
            return {}
    else:
        quake_list = []
        query = collection.find({"country": country}).sort("time", -1)
        if limit is not None:
            query = query.limit(limit)
        for quake in query:
            quake["_id"] = str(quake["_id"])
            quake_list.append(quake)
        return quake_list


def classify_magnitude(magnitude):
    """
    Clasifica la magnitud de un terremoto en una categoría específica.

    Parámetros:
    - magnitude (float): Magnitud del terremoto.

    Retorna:
    - categoría (str): Categoría a la que pertenece la magnitud del terremoto.
    """
    if 0.0 <= magnitude <= 4.0:
        return "Generalmente no se siente, pero es registrado"
    elif 4.0 <= magnitude <= 6.0:
        return "Ocasiona daños ligeros a edificios"
    elif 6.0 <= magnitude <= 6.9:
        return "Puede ocasionar daños severos en áreas donde vive mucha gente"
    elif 7.0 <= magnitude <= 7.9:
        return "Terremoto mayor. Causa graves daños"
    elif magnitude >= 8.0:
        return "Gran terremoto. Destrucción total a comunidades cercanas"
    else:
        return "Magnitud no clasificada"

@app.get("/classf")
async def predict_quake(depth: float, magnitude: float):
    """
    Realiza una predicción de clasificación de terremotos utilizando el modelo entrenado.

    Parámetros:
    - depth (float): Profundidad del terremoto.
    - magnitude (float): Magnitud del terremoto.

    Retorna:
    - classification (list): Lista de etiquetas de clasificación para el terremoto.
    - alert (str): Alerta asociada a la magnitud del terremoto.
    """

    # Transformar los datos de entrada en la forma que el modelo espera
    input_data = [[depth, magnitude]]

    # Hacer la predicción
    prediction = model.predict(input_data)
    dict_depth = {0: "profundo", 1: "superficial", 2: "semi-profundo", 3: "intermedio"}

    # Función para mapear los valores del array a las etiquetas correspondientes
    map_func = np.vectorize(lambda x: dict_depth[x])
    # Aplicar el mapeo al array
    mapped_array = map_func(prediction)

    alert = classify_magnitude(input_data[0][1])

    # Devolver la predicción
    return {"classification": mapped_array.tolist(), "alert": alert}


@app.get("/user_data", response_model=List[User])
async def read_users(
    countries: Optional[List[str]] = Query(None),
    id_chats: Optional[List[str]] = Query(None),
):
    """
    Devuelve los usuarios que cumplen con las condiciones de búsqueda en la base de datos. Si no se proporciona ningún
    criterio, se devolverán todos los usuarios.
    """
    query = {}
    if countries is not None:
        query["country"] = {"$in": countries}
    if id_chats is not None:
        query["id_chat"] = {"$in": id_chats}
    users = user_collection.find(query)
    return [User(**user) for user in users]


@app.post("/user", response_model=User)
async def create_user(user: User):
    """
    Esta función registra el nuevo usuario del bot en la base de datos de Mongo "users".
    """
    if hasattr(user, "id"):
        delattr(user, "id")
    user_data = user.dict()
    user_data["id_chat"] = str(user_data["id_chat"])
    user_id = user_collection.insert_one(user_data)  # Inserta los datos en la colección
    user_data["id"] = str(user_id.inserted_id)  # Convierte el ObjectId a str
    return user_data  # Devuelve los datos de usuario con el id incluido


@app.on_event("shutdown")
def shutdown_event():
    client.close()
