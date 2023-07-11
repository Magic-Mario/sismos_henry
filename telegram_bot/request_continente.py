import requests
def obtener_paises_por_continente(continente):
    url = f"https://restcountries.com/v3.1/region/{continente}"
    response = requests.get(url)

    if response.status_code == 200:
        datos = response.json()
        paises = [pais['name']['common'] for pais in datos]
        return paises
    else:
        print("Error al obtener la lista de países:", response.status_code)
        return None

# Ejemplo de uso
continente = "africa"
paises = obtener_paises_por_continente(continente)
if paises:
    print(f"Países en {continente}:")
    for pais in paises:
        print(pais)

print("-\n".join(paises))


def obtener_pai(pais):
    url = f"https://restcountries.com/v2/name/{pais}"
    response = requests.get(url)

    if response.status_code == 200:
        datos = response.json()
        print(datos)
        datos = [dato['latlng'] for dato in datos]
        return datos[0]
    else:
        print("Error al obtener la lista de países:", response.status_code)
        return None
    
print(obtener_pai('chile'))

