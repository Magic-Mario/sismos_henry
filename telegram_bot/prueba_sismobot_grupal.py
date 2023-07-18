from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import datetime
import os
import schedule
import time
import random


# Crear un diccionario para mapear los IDs a las opciones de 'place'
places_por_id = {
    "64b6b4eca42c41e512af5b28": [
        "PRUEBABOT: 27 km E of Cordova, Alaska",
        "PRUEBABOT: 9 km WNW of Cobb, CA",
        "PRUEBABOT: 4 km SE of Pāhala, Hawaii"
    ],
    "64b6aa60a42c41e512af5b27": [
        "PRUEBABOT: Volcano Islands, Japan region",
        "PRUEBABOT: 11 km SSE of Asahi, Japan",
        "PRUEBABOT: 27 km SE of Shinmachi, Japan"
    ],
    "64b6a46fa42c41e512af5b26": [
        "PRUEBABOT: 47 km W of Valparaíso, Chile",
        "PRUEBABOT: 33 km WNW of Hacienda La Calera, Chile",
        "PRUEBABOT: 31 km ENE of Chicureo Abajo, Chile"
    ]
}

# Crear una función para el trabajo que quieres realizar
def actualizar_mongo():

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
        "64b6b4eca42c41e512af5b28"
    ]


    # Crear la lista de nuevos tiempos con intervalos de 30 segundos a partir del tiempo actual
    #tiempo_actual = datetime.datetime.now()
    tiempo_actual = datetime.datetime.utcnow()  # Usar utcnow en lugar de now

    print(tiempo_actual)
    nuevos_valores_time = [
        tiempo_actual + datetime.timedelta(seconds=i*15)
        for i in range(len(ids_a_actualizar))] #lista con los valores de tiempo a reemplazar con el formato requerido por BSON

    print(nuevos_valores_time)

    # Iterar sobre los IDs y actualizar cada documento
    for id_, nuevo_time in zip(ids_a_actualizar, nuevos_valores_time):
        # Generar valores aleatorios para 'dep' y 'mag'
        nuevo_dep = random.randint(10, 999)
        nuevo_mag = random.uniform(1, 10)  # Esto genera un float entre 1 y 10

        # Seleccionar una opción aleatoria de 'place' para este ID
        nuevo_place = random.choice(places_por_id[id_])

        # Actualizar el documento
        collection.update_one(
            {"_id": ObjectId(id_)},
            {"$set": {"time": nuevo_time, "depth": nuevo_dep, "mag": nuevo_mag, "place": nuevo_place}}
        )
# Configurar schedule para ejecutar tu función cada 2 minutos
schedule.every(1).minutes.do(actualizar_mongo)

# Ejecutar schedule en un bucle infinito
while True:
    schedule.run_pending()
    time.sleep(1)        