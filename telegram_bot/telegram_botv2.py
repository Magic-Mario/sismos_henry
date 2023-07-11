from configuracion import * #del archivo configuración, recojo el token
import telebot # manejar la api de telegram
import requests
import schedule
import datetime as dt 
from telebot.types import ReplyKeyboardMarkup #crear los botones
from telebot.types import ReplyKeyboardRemove # para eliminar los botones


bot = telebot.TeleBot(token) #creo el bot

#definición de los botones:
botones = ReplyKeyboardMarkup(one_time_keyboard=True,
                                  input_field_placeholder="Pulsa un botón",
                                  resize_keyboard=True
                                 ) #los botones que coloque, se borraran al hundirlos
#creamos los 2 botones
botones.add("acepto", "no acepto")

#Datos de los usuarios
usuario = {'permiso':'',
           'locacion': {'continente': '',
                        'pais':'',
                        'lat':'',
                        'lon':''}}


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
        if datos[0] != None:
            datos = datos[0]['properties']

            mensaje = f"Hubo un terremoto cercano a ti, a {datos['place']}\nCon una magnitud de {datos['mag']}\n¿Te encuentras bien?"
            
            return mensaje
    else:
        print("Error al realizar la solicitud:", response.status_code)

@bot.message_handler(commands=['start'])
def comando_start(mensaje):
    #Mensaje de bienvenida

    bot.send_message(mensaje.chat.id, "Bienvenido, soy Sismobot, y te notificaré si hay terremotos en tu zona, pero antes, necesito pedirte un permiso: ")

    # preguntamos si acepta que sepamos su ubicación (lo coloco pero no hace nada)
    msg = bot.send_message(mensaje.chat.id,'Aceptas que tengamos tu ubicación',reply_markup=botones)
    #guardamos el resultado en una variable con un función
    bot.register_next_step_handler(msg, permiso_y_continente)

def permiso_y_continente(mensaje):
    """Guardamos el permiso del usuario """

    botones_continente = ReplyKeyboardMarkup(one_time_keyboard=True,
                                  input_field_placeholder="Pulsa un botón",
                                  resize_keyboard=True
                                 ) #los botones que coloque, se borraran al hundirlos
    #creamos los 5 botones
    botones_continente.add("America", "Europa", "Asia", "Africa", "Oceania")

    #si el listillo escribe en vez de usar los botones:
    if mensaje.text != "acepto" and mensaje.text != "no acepto":
        #le decimos al usuario que escoja una opción valida de los bontones:
        msg = bot.send_message(mensaje.chat.id, "ERROR: Opción no valida.\nEscoge una opción de los botones", reply_markup=botones)
        #vuelvo a repetir la función para guardar
        bot.register_next_step_handler(msg,permiso_y_continente)
    elif mensaje.text == "no acepto":
        msg = bot.send_message(mensaje.chat.id, "Está bien, siendo el caso, no podré notificarte. En caso de querer reiniciar el proceso, presiona /start")
    else: #por si coloco una respuesta correcta
        msg = bot.send_message(mensaje.chat.id, "Perfecto, en que continente te encuentras? ", reply_markup= botones_continente)
        usuario["permiso"] = mensaje.text
        bot.register_next_step_handler(msg,ubicacion_continente)
    

def ubicacion_continente(mensaje):
    #modifico el nombre de los Continentes para depueés buscarlos en la API
    continentes = {"America": 'Americas', "Europa" : 'Europe', "Asia" : "Asia", "Africa": "Africa", "Oceania": "Oceania"}
    usuario["locacion"]['continente'] = continentes[mensaje.text]
    #busco los continentes para sacar los paises que este contiene
    paises = obtener_paises_por_continente(usuario["locacion"]['continente'])
    #hago una lista de los paises para luego mostrarlas en un mensaje de Telegram
    paises = "\n".join(paises)
    #Muestro los paises y espero que el usuario escriba uno de esos paises
    msg = bot.send_message(mensaje.chat.id, f"De los siguientes paises, dónde te encuentras? \n{paises}")
    bot.register_next_step_handler(msg, ubicacion_pais)

def ubicacion_pais(mensaje):
    #guardo el pais en el usuario
    usuario["locacion"]['pais'] = mensaje.text
    #Encuento las coordenadas del pais  por la API
    datos = obtener_pais(usuario["locacion"]['pais'])
    # Guardo las coordenadas
    usuario["locacion"]['lat']= datos[0]
    usuario["locacion"]['lon']= datos[1]

    bot.send_message(mensaje.chat.id, f"Con esta información, te mantendré al tanto de los terremotos en tu area. ^^")
    print(usuario)
    bot.register_next_step_handler(mensaje,bucle_tiempo)

def bucle_tiempo(mensaje):
    terremoto = obtener_terremoto()
    bot.send_message(mensaje.chat.id, terremoto)



if __name__ == '__main__':
    print( 'EL bot está en funcionamiento')

    #El siguiente bucle manda un bip para saber si aún está funcionando el bot
    
    bot.infinity_polling() #bucle infinito donde se revisa si hay nuevos mensajes
