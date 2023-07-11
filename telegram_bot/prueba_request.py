import requests
import json
import datetime as dt

latitud = 4.0
longitud = -72.0

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Parámetros de la solicitud
parametros = {
    "format": "geojson",
    "endtime": "YYYY-MM-DD",
    "latitude": latitud,
    "longitude": longitud,
    "maxradiuskm": 100,
}

# Obtener la fecha actual
fecha_actual = dt.date.today()
fecha_actual_str = fecha_actual.strftime("%Y-%m-%d")

# Actualizar los parámetros de la solicitud con la fecha actual
parametros["endtime"] = fecha_actual_str

# Realizar la solicitud GET a la API de la USGS
response = requests.get(url, params=parametros)

# Verificar el código de estado de la respuesta
if response.status_code == 200:
    # Obtener los datos en formato JSON
    datos_json = response.json()
    # Guardar los datos en un archivo GeoJSON
    print(datos_json)
else:
    print("Error al realizar la solicitud:", response.status_code)