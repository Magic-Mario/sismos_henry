import requests

base_url = "https://henrypf-sismos-prueba.onrender.com"  # ruta a la API
#base_url = "http://127.0.0.1:8000"  # ruta a la API


# # Test /date/ endpoint
limit = 5
start_date = "01/01/23"
end_date = "03/02/23"
response = requests.get(f"{base_url}/date/", params={"start_date": start_date, "end_date": end_date, 'limit': limit})
print(f"Prueba #1 \n /date/ endpoint response: {response.json()}")

# Test /magnitude/{min_magnitude}/{max_magnitude} endpoint
min_magnitude = 7
max_magnitude = 8
response = requests.get(f"{base_url}/magnitude/{min_magnitude}/{max_magnitude}", params={'limit': limit})
print(f"Prueba #2 \n /magnitude/{min_magnitude}/{max_magnitude} endpoint response: {response.json()}")

# Test /depth/{min_depth}/{max_depth} endpoint
min_depth = 90
max_depth = 100
response = requests.get(f"{base_url}/depth/{min_depth}/{max_depth}", params={'limit': limit})
print(f"Prueba #3 \n /depth/{min_depth}/{max_depth} endpoint response: {response.json()}")

# Test /country/{country} endpoint
#prueba con último registro
country = 'usa'
latest = True
response = requests.get(f"{base_url}/country/{country}", params={'latest': latest})
print(f"Prueba #4 \n /country/{country}?latest={latest} endpoint response: {response.json()}")

#prueba con limite
country = 'japan'
response = requests.get(f"{base_url}/country/{country}", params={'limit': limit})
print(f"Prueba #5 \n /country/{country}?latest={latest} endpoint response: {response.json()}")

# Test /classf endpoint
response = requests.get(f"{base_url}/classf", params={"depth": max_depth, "magnitude": max_magnitude})
print(f"Prueba #6 \n /classf endpoint response: {response.json()}")
