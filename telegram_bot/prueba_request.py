import requests
import json
import datetime as dt

latitud = -30.0
longitud = -71.0

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
"""latitud = usuario['locacion']['lat']
longitud = usuario['locacion']['lon']"""

# Parámetros de la solicitud
parametros = {
    "format": "geojson",
    "latitude": latitud,
    "longitude": longitud,
    "maxradiuskm": 100,
    "limit":1
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
    datos = response.json()
    #se extrae la información que se necesita del geojson
    datos = datos['features']
    # Verifico que si hayan datos disponibles
    if datos:
        datos = datos[0]['properties']

        mensaje = f"Hubo un terremoto cercano a ti, a {datos['place']}\nCon una magnitud de {datos['mag']}\n¿Te encuentras bien?"
        
        print(mensaje)
else:
    print("Error al realizar la solicitud:", response.status_code)


"""{'type': 'FeatureCollection',
  'metadata': {
      'generated': 1689045067000,
        'url': 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&latitude=-30.0&longitude=-71.0&maxradiuskm=1000&limit=1&endtime=2023-07-10',
        'title': 'USGS Earthquakes', 
        'status': 200, 
        'api': '1.14.0', 
        'limit': 1, 
        'offset': 1, 
        'count': 1}, 
    'features': [
        {'type': 'Feature',
          'properties': {'mag': 5.6,
                        'place': '31 km ENE of Chicureo Abajo, Chile',
                        'time': 1688922693953, 
                        'updated': 1689016112040, 
                        'tz': None, 
                        'url': 'https://earthquake.usgs.gov/earthquakes/eventpage/us6000kr5g', 
                        'detail': 'https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=us6000kr5g&format=geojson', 
                        'felt': 135, 
                        'cdi': 5.6, 
                        'mmi': 4.975, 
                        'alert': 
                        'green', 
                        'status': 'reviewed', 
                        'tsunami': 0, 
                        'sig': 558, 
                        'net': 'us', 
                        'code': 
                        '6000kr5g', 
                        'ids': ',us6000kr5g,usauto6000kr5g,', 
                        'sources': ',us,usauto,', 
                        'types': ',dyfi,internal-moment-tensor,losspager,moment-tensor,origin,phase-data,shakemap,', 
                        'nst': 98, 
                        'dmin': 0.252, 
                        'rms': 0.73, 
                        'gap': 42, 
                        'magType': 
                        'mww', 
                        'type': 
                        'earthquake', 
                        'title': 
                        'M 5.6 - 31 km ENE of Chicureo Abajo, Chile'}, 
        'geometry': {'type': 'Point', 'coordinates': [-70.3268, -33.2122, 101.785]}, 'id': 'us6000kr5g'}]}"""