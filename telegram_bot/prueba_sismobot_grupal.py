from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import datetime
import os


# definición de constantes
#clave para acceder a mongo
# password = os.getenv("MONGODB_PASSWORD")
#print(password)
password = 'picassojp'

# Crear un nuevo cliente y conectarse al servidor
uri = f"mongodb+srv://picassojp:{password}@cluster0.cchanol.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["pf-henry"]
collection = db["db-pf-henry"]

# Definir los IDs de los documentos a actualizar y los nuevos valores de 'time'
ids_a_actualizar = [
    "64b6a46fa42c41e512af5b26",
    "64b6aa60a42c41e512af5b27",
    "64b6b4eca42c41e512af5b28",
    "64b6b551a42c41e512af5b29",
    "64b6b595a42c41e512af5b2a",
    "64b6b5b3a42c41e512af5b2b",
    "64b6b5cba42c41e512af5b2c",
    "64b6b5e0a42c41e512af5b2d",
    "64b6b5f1a42c41e512af5b2e"
]


# Definir los nuevos valores para 'time'
nuevos_valores_time = [
    datetime.datetime(2023, 7, 18, 21, 30, 2, 632905),
    datetime.datetime(2023, 7, 18, 21, 31, 2, 632905),
    datetime.datetime(2023, 7, 18, 21, 32, 2, 632905),
    datetime.datetime(2023, 7, 18, 21, 33, 2, 632905),
    datetime.datetime(2023, 7, 18, 21, 34, 2, 632905),
    datetime.datetime(2023, 7, 18, 21, 35, 2, 632905),
    datetime.datetime(2023, 7, 18, 21, 36, 2, 632905),
    datetime.datetime(2023, 7, 18, 21, 37, 2, 632905),
    datetime.datetime(2023, 7, 18, 21, 38, 2, 632905)
]

# Crear la lista de nuevos tiempos con intervalos de 30 segundos a partir del tiempo actual
#tiempo_actual = datetime.datetime.now()
tiempo_actual = datetime.datetime.utcnow()  # Usar utcnow en lugar de now

print(tiempo_actual)
# nuevos_valores_time = [
#     tiempo_actual + datetime.timedelta(seconds=i*30)
#     for i in range(len(ids_a_actualizar))] #lista con los valores de tiempo a reemplazar con el formato requerido por BSON

print(nuevos_valores_time)

# Iterar sobre los IDs y actualizar cada documento
for id_, nuevo_time in zip(ids_a_actualizar, nuevos_valores_time):
    collection.update_one({"_id": ObjectId(id_)}, {"$set": {"time": nuevo_time}})