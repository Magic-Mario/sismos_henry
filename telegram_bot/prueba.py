import requests #hacer las peticiones a las api
consulta_clasificacion = requests.get(f"https://henrypf-sismos-prueba.onrender.com/classf?depth={5}&magnitude={2}")
#Convierto la consulta en json
datos_clasificacion = consulta_clasificacion.json()

print(datos_clasificacion['classification'][0])
print(datos_clasificacion['alert'])
