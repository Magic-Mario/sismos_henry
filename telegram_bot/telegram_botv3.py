from configuracion import * # el archivo configuración, recojo el token
import telebot # manejar la api de telegram
import requests #hacer las peticiones a las api
import schedule #hacer tareas para cumplir
import datetime as dt #modificar las fechas de la api gringa
import time
from telebot.types import ReplyKeyboardMarkup #crear los botones


bot = telebot.TeleBot(token) #creo el bot

#definición de los botones:
botones = ReplyKeyboardMarkup(one_time_keyboard=True,
                                  input_field_placeholder="Pulsa un botón",
                                  resize_keyboard=True
                                 ) #los botones que coloque, se borraran al hundirlos
#creamos los 2 botones
botones.add("Acepto", "No acepto")


botones_pais = ReplyKeyboardMarkup(one_time_keyboard=True,
                                input_field_placeholder="Pulsa un botón",
                                resize_keyboard=True
                                ) #los botones que coloque, se borraran al hundirlos
#creamos los 3 botones de los paises
botones_pais.add("Estados Unidos", "Chile", "Japón")



#Datos de los usuarios
usuario = {'permiso':'',
           'locacion': {'pais':'',
                        'lat':'',
                        'lon':''}}



def obtener_pais(pais):
    url = f"https://restcountries.com/v2/name/{pais}"
    response = requests.get(url)

    if response.status_code == 200:
        datos = response.json()
        datos = [dato['latlng'] for dato in datos]
        return datos[0]
    else:
        print("Error al obtener la lista de países:", response.status_code)
        return None    



def obtener_terremoto():
    if usuario['locacion']['lon'] != '' and  usuario['locacion']['lat'] != '':

        url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        latitud = usuario['locacion']['lat']
        longitud = usuario['locacion']['lon']

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
                
                return mensaje
            else:

                mensaje = "No ha pasado nada"

                return mensaje
        else:
            print("Error al realizar la solicitud:", response.status_code)


def reporte_terremoto(mensaje):
    terremoto = obtener_terremoto()

    if terremoto != "No ha pasado nada":
        bot.send_message(mensaje.chat.id, terremoto)

@bot.message_handler(commands=['start'])
def comando_start(mensaje):
    #Mensaje de bienvenida

    bot.send_message(mensaje.chat.id, "Bienvenido, soy Sismobot, y te notificaré si hay terremotos en tu zona, pero antes, necesito pedirte un permiso: ")

    # preguntamos si acepta que sepamos su ubicación (lo coloco pero no hace nada)
    msg = bot.send_message(mensaje.chat.id,'Aceptas que tengamos tu ubicación',reply_markup=botones)

    #guardamos el resultado en una variable con un función
    bot.register_next_step_handler(msg, permiso)



def permiso(mensaje):
    """Guardamos el permiso del usuario """

    #si el listillo escribe en vez de usar los botones:
    if mensaje.text != "Acepto" and mensaje.text != "No acepto":
        #le decimos al usuario que escoja una opción valida de los bontones:
        msg = bot.send_message(mensaje.chat.id, "ERROR: Opción no valida.\nEscoge una opción de los botones", reply_markup=botones)
        #vuelvo a repetir la función para guardar
        bot.register_next_step_handler(msg,permiso)
    elif mensaje.text == "no acepto":
        msg = bot.send_message(mensaje.chat.id, "Está bien, siendo el caso, no podré notificarte. En caso de querer reiniciar el proceso, presiona /start")
    else: #por si coloco una respuesta correcta
        msg = bot.send_message(mensaje.chat.id, "Perfecto, en qué pais te encuentras? ", reply_markup= botones_pais)
        usuario["permiso"] = mensaje.text
        bot.register_next_step_handler(msg,ubicacion_pais)
    


def ubicacion_pais(mensaje):
    #consulto si el pais que escogió sí está en la lista de los paises
    if mensaje.text != "Estados Unidos" and mensaje.text != "Chile" and mensaje.text != "Japón" :
        #le decimos al usuario que escoja una opción valida de los bontones:
        msg = bot.send_message(mensaje.chat.id, "ERROR: Opción no valida.\nEscoge una opción de los botones", reply_markup=botones_pais)
        #vuelvo a repetir la función para guardar
        bot.register_next_step_handler(msg,ubicacion_pais)
    else:
        #modifico el string del pais para poder buscarlo
        paises = {"Estados Unidos":"United States of America","Japón":"Japan","Chile":"Chile"}
        #guardo el pais en el usuario
        
        usuario["locacion"]['pais'] = paises[mensaje.text]
        #Encuento las coordenadas del pais  por la API
        datos = obtener_pais(usuario["locacion"]['pais'])
        # Guardo las coordenadas
        usuario["locacion"]['lat']= datos[0]
        usuario["locacion"]['lon']= datos[1]

        bot.send_message(mensaje.chat.id, f"Con esta información, te mantendré al tanto de los terremotos en tu area. ^^ \nEn caso de querer detener el bot, presiona o escribe /stop")

        # Comienza el bucle de mandar reportes de terremotos
        schedule.every(20).seconds.do(reporte_terremoto,mensaje)
        while True:
            schedule.run_pending()
            time.sleep(10)

@bot.message_handler(commands=['stop'])
def detener(mensaje):
    bot.send_message(mensaje.chat.id, f"Se ha detenido el bot, si deseas volver a iniciarlo, presiona: /start.")
    schedule.clear()
    


if __name__ == '__main__':
    print( 'EL bot está en funcionamiento')
    bot.infinity_polling() #bucle infinito donde se revisa si hay nuevos mensajes

