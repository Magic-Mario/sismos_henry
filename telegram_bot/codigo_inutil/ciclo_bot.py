from configuracion import * # el archivo configuración, recojo el token
import telebot # manejar la api de telegram
import requests #hacer las peticiones a las api
import schedule #hacer tareas para cumplir
import datetime as dt #modificar las fechas de la api gringa
import time



bot = telebot.TeleBot(token) #creo el bot

#definición de los botones:

paises =['usa','japan','chile']
def informar_terremoto():
    for pais in paises:
        # Realizar la solicitud GET a la API de la USGS
        consulta_pais = requests.get(f"https://henrypf-sismos-prueba.onrender.com/country/{pais}?latest=true")

        # Hacer la consulta de los usuarios de ese pais

        # Verificar el código de estado de la respuesta
        if consulta_pais.status_code == 200:

            # Obtener los datos en formato JSON
            datos = consulta_pais.json()

            #se extrae la información que se necesita del geojson

            # Verifico que si hayan datos disponibles
            if datos:

                tiempo = dt.datetime.strptime(datos['time'],"%Y-%m-%dT%H:%M:%S.%f")
                fecha = tiempo.strftime("%Y-%m-%d")

                tiempo_actual = dt.datetime.now()
                fecha_actual = tiempo_actual.strftime("%Y-%m-%d")

                if fecha == fecha_actual:

                    hora = tiempo.time()
                    hora_actual = tiempo_actual.time()
                    diferencia = (dt.datetime.combine(dt.date.min, hora_actual) - dt.datetime.combine(dt.date.min, hora)).seconds
                    una_hora = dt.timedelta(hours=1)

                    if diferencia >= una_hora.total_seconds():

                        mensaje = f"Se identifico un terremoto a las {hora}.\nCon una magnitud de {datos['mag']} y profundidad de {datos['depth']} km.\nA {datos['place']}.\n¿Te encuentras bien?"

                    else:

                        mensaje = "ho ha pasado nada"
                    
                    return( mensaje)
                else:
                    mensaje = "No ha pasado nada"

                    return(mensaje)

            else:

                mensaje = "No ha pasado nada"

                return(mensaje)
        else:
            print("Error al realizar la solicitud:", consulta_pais.status_code)



def reporte_terremoto(mensaje):
    terremoto = informar_terremoto()
    
    if terremoto != "No ha pasado nada":
        bot.send_message(mensaje.chat.id, terremoto)



"""
        schedule.every(15).minutes.do(reporte_terremoto,mensaje)
        while True:
            schedule.run_pending()
            time.sleep(60)"""

    


if __name__ == '__main__':
    print( 'EL bot está en funcionamiento')
    bot.infinity_polling() #bucle infinito donde se revisa si hay nuevos mensajes
