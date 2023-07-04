#!/usr/bin/env python
# coding: utf-8


# se cargan las librerías necesarias
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
from datetime import datetime


# # 1. Extracción de datos de la página web de la Japan Meteorological Agency


# hora actual
now = datetime.now()
# formato dd/mm/YY
d1 = now.strftime("%d-%m-%Y-%H%M")


# ruta para guardar el df con los datos scrapeados
ruta_df_japon = f"datasets/japan_scrapped_dataset-{d1}.csv"


# Configura las opciones de Chrome para ejecutar en modo headless (sin interfaz gráfica)
chrome_options = Options()
chrome_options.add_argument("--headless")

# Configura el webdriver
webdriver_service = Service(ChromeDriverManager().install())


driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
# Accede a la página web
driver.get("https://www.data.jma.go.jp/multi/quake/index.html?lang=es")


# Permite que la página cargue
time.sleep(5)

# Obtiene el elemento de la tabla
table = driver.find_element(By.XPATH, '//*[@id="quakeindex_table"]')


# Extrae los datos y los href de la tabla
table_data = []
rows = table.find_elements(By.TAG_NAME, "tr")

# cantidad de filas
print(len(rows))

# Espera a que se carguen las filas
wait = WebDriverWait(driver, 10)

for row in rows[1:]:
    # print(row)
    cols = row.find_elements(By.TAG_NAME, "td")
    row_data = [ele.text for ele in cols]
    hrefs = [
        ele.find_element(By.TAG_NAME, "a").get_attribute("href")
        if ele.find_elements(By.TAG_NAME, "a")
        else None
        for ele in cols
    ]
    row_data.extend([ele for ele in hrefs if ele])

    # Para cada href, visita la página y extrae más información
    for href in row_data[-1:]:
        # Abre una nueva pestaña
        driver.execute_script("window.open('');")

        # Cambia a la nueva pestaña (suponiendo que es la última a la derecha)
        driver.switch_to.window(driver.window_handles[-1])

        # Visita la página del href
        driver.get(href)

        # Espera a que se cargue la nueva página
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="quakeindex_table"]/tbody/tr[2]')
            )
        )

        # Extrae más información de la nueva página
        elements = driver.find_elements(
            By.XPATH, '//*[@id="quakeindex_table"]/tbody/tr[2]/td'
        )
        additional_info = [ele.text for ele in elements]

        # Añade la nueva información a los datos de la fila
        row_data.extend(additional_info)
        print(row_data)

        # Cierra la pestaña actual
        driver.close()

        # Cambia de nuevo a la pestaña original
        driver.switch_to.window(driver.window_handles[0])

        wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="quakeindex_table"]'))
        )
    # apendea todos los registros
    table_data.append(row_data)


# Convierte los datos de la tabla a un DataFrame
df = pd.DataFrame(table_data)


# Cierra el webdriver
driver.quit()


df.columns  # nombres de las columnas


# cambiar nombres de columnas
df = df.rename(
    columns={
        0: "det_fecha_hora",
        1: "epi",
        2: "mag",
        3: "int_max",
        4: "emis_fecha_hora",
        5: "href",
        6: "det_fecha_hora_local",
        7: "lat",
        8: "lon",
        9: "mag_2",
        10: "prof_epi",
        11: "epi_2",
    }
)


df.drop(
    labels=["mag_2", "epi_2"], axis=1, inplace=True
)  # se eliminan las columnas redundantes


# dimensiones del df
df.shape


# muestra del df
df.head()


# # 2. Preprocesamiento

# #### se crea la columna "id"


df.href.unique()  # se revisa la columna href para definir un id para cada registro


df["id"] = df["href"].str.extract("eventID=(\d+)&")  # se extrae el ID del evento
df["id"] = df["id"].astype("Int64")  # se cambia el formato a int


# #### se cambia el formato de la variable profundidad del epicentro


# extrae los números de km y convierte a tipo float
df["prof_epi_nro"] = df["prof_epi"].str.extract("(\d+)").astype(float)

# reemplaza los NaN (que corresponden a "Poco profundo") por 1
df["prof_epi_nro"].fillna(1, inplace=True)


# #### se cambia el formato de las coordenadas geográficas


# cambia los nombres de las columnas originales
df.rename(columns={"lat": "lat_0", "lon": "lon_0"}, inplace=True)

# extrae los números y convierte a tipo float
df["lat"] = df["lat_0"].str.extract("(\d+.\d+)").astype(float)
df["lon"] = df["lon_0"].str.extract("(\d+.\d+)").astype(float)

# cambia los valores negativos para los que están en el hemisferio sur y oeste
df["lat"] = df["lat"].where(~df["lat_0"].str.contains("S"), -df["lat"])
df["lon"] = df["lon"].where(~df["lon_0"].str.contains("O"), -df["lon"])


# #### cambia formato de columnas de fecha


df["det_fecha_hora"] = pd.to_datetime(df["det_fecha_hora"])
df["emis_fecha_hora"] = pd.to_datetime(df["emis_fecha_hora"])
df["det_fecha_hora_local"] = pd.to_datetime(df["det_fecha_hora_local"])


df.head()  # muestra de las primeras filas


df.to_csv(ruta_df_japon, index=False)  # guarda el df
