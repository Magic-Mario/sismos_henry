from configuracion import * #del archivo configuración, recojo el token
import telebot # manejar la api de telegram
import requests
import schedule 
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

#función del heart-rate
def trabajo():
    print('sigues allí?')

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
    continentes = {"America": 'Americas', "Europa" : 'Europe', "Asia" : "Asia", "Africa": "Africa", "Oceania": "Oceania"}
    usuario["locacion"]['continente'] = continentes[mensaje.text]
    paises = obtener_paises_por_continente(usuario["locacion"]['continente'])
    paises = "\n".join(paises)
    msg = bot.send_message(mensaje.chat.id, f"De los siguientes paises, dónde te encuentras? \n{paises}")
    bot.register_next_step_handler(msg, ubicacion_pais)

def ubicacion_pais(mensaje):
    usuario["locacion"]['pais'] = mensaje.text

    datos = obtener_pais(usuario["locacion"]['pais'])

    usuario["locacion"]['lat']= datos[0]
    usuario["locacion"]['lon']= datos[1]

    bot.send_message(mensaje.chat.id, f"Con esta información, te mantendré al tanto de los terremotos en tu area. ^^")


if __name__ == '__main__':
    print( 'EL bot está en funcionamiento')

    #El siguiente bucle manda un bip para saber si aún está funcionando el bot
    """schedule.every(30).seconds.do(trabajo)
    while True:
        schedule.run_pending()"""
    bot.infinity_polling() #bucle infinito donde se revisa si hay nuevos mensajes
