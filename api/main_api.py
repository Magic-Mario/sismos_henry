from fastapi import FastAPI, Path
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import os

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

#datos para acceder a la base de datos
uri = f"mongodb+srv://picassojp:{password}@cluster0.cchanol.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["pf-henry"] #base de datos
collection = db["db-pf-henry"] #colección

@app.get("/date/")
async def get_quakes_by_date(start_date: str, end_date: str):
    """
    Esta función devuelve una lista con todos los registros de sismos entre dos fechas.
    """
    
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

    quake_list = []

    for quake in collection.find({'time': {'$gte': start_date_obj, '$lte': end_date_obj}}): #se filtran los documentos según los valores de fechas
        quake["_id"] = str(quake["_id"]) #se modifica el formato del id de mongodb (bson)
        quake_list.append(quake) # se apendean los documentos en una lista
    return quake_list

@app.get("/magnitude/{min_magnitude}/{max_magnitude}")
async def get_quakes_by_magnitude(min_magnitude: float = Path(0.0), max_magnitude: float = Path(10.0)):
    """
    Esta función devuelve todos los registros de sismos según una magnitud mínima y una máxima. De forma predeterminada estos valores corresponden a los límites de la escala (0-10)
    """
    quake_list = []
    for quake in collection.find({"mag": {"$gte": min_magnitude, "$lte": max_magnitude}}): #se filtran los documentos según los valores de magnitud
        quake["_id"] = str(quake["_id"]) #se modifica el formato del id de mongodb (bson)
        quake_list.append(quake) # se apendean los documentos en una lista
    return quake_list


@app.get("/depth/{min_depth}/{max_depth}")
async def get_quakes_by_depth(min_depth: float = Path(0), max_depth: float = Path(1000)):
    """
    Esta función devuelve todos los registros de sismos según una profundidad mínima y una máxima expresada en kilómetros. De forma predeterminada estos valores corresponden a los límites típicos (0-1000)
    """
    quake_list = []
    for quake in collection.find({"depth": {"$gte": min_depth, "$lte": max_depth}}): #se filtran los documentos según los valores de profundidad
        quake["_id"] = str(quake["_id"]) #se modifica el formato del id de mongodb (bson)
        quake_list.append(quake) # se apendean los documentos en una lista
    return quake_list

@app.get("/country/{country}")
async def get_quakes_by_country(country: str, latest: bool = False):
    """
    Esta función devuelve todos los registros de sismos según alguno de los tres países posibles: usa, japan y chile.
    Si latest es True, devuelve solo el registro más reciente.
    """
    if latest:
        cursor = collection.find({"country": country}, 
                                {"_id": 1, "id": 1, "mag": 1, "depth": 1}).sort("time", -1).limit(1) #se usa la proyección de mongoDB para filtrar las variables de interés, se ordenan de forma decreciente y se limita la salida a 1
        try:
            quake = next(cursor)
            quake["_id"] = str(quake["_id"])
            return quake
        except StopIteration: #maneja la excepción de que la consulta no devuelva ningún registro
            return {}
    else:
        quake_list = []
        for quake in collection.find({"country": country}):
            quake["_id"] = str(quake["_id"])
            quake_list.append(quake)
        return quake_list

@app.on_event("shutdown")
def shutdown_event():
    client.close()
