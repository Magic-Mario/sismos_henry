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
usuario = {'codigo':'',
           'pais':''}





@bot.message_handler(commands=['start'])
def comando_start(mensaje):
    #Mensaje de bienvenida

    bot.send_message(mensaje.chat.id, "Bienvenido, soy Sismobot, y te notificaré si hay terremotos en tu zona, pero antes, necesito pedirte un permiso: ")

    # preguntamos si acepta que sepamos su ubicación (lo coloco pero no hace nada)
    msg = bot.send_message(mensaje.chat.id,'Aceptas que tengamos tu ubicación?\n(Abajo encontrarás los botones de respuesta, en caso de estar en web, presionar el simbolo al lado de adjuntar archivos)',reply_markup=botones)

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
    elif mensaje.text == "No acepto":
        msg = bot.send_message(mensaje.chat.id, "Está bien, siendo el caso, no podré notificarte. En caso de querer reiniciar el proceso, presiona --> /start <--")
    else: #por si coloco una respuesta correcta
        msg = bot.send_message(mensaje.chat.id, "Perfecto, en qué pais te encuentras? ", reply_markup= botones_pais)
        usuario["codigo"] = mensaje.chat.id
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
        paises = {"Estados Unidos":"usa","Japón":"japan","Chile":"chile"}
        #guardo el pais en el usuario
        usuario['pais'] = paises[mensaje.text]
        bot.send_message(mensaje.chat.id, f"Con esta información, te mantendré al tanto de los terremotos en tu area. ^^ \nEn caso de querer detener el bot, presiona o escribe --> /stop <--")

        #monto los datos 
        #url = "https://henrypf-sismos-prueba.onrender.com/user"
        #data = {"id_chat": mensaje.chat.id, "country":usuario['pais']}
        #consulta_pais = requests.post(url, json=data)


        # Guardo los datos en la aplicación
        with open("documento.txt", "a") as archivo:
        # Agregar el contenido al final del archivo
            archivo.write( str(usuario['codigo']) +","+usuario['pais'] + "\n")






@bot.message_handler(commands=['stop'])
def detener(mensaje):
    bot.send_message(mensaje.chat.id, f"Se ha detenido el bot, si deseas volver a iniciarlo, presiona: --> /start <--")

    


if __name__ == '__main__':
    print( 'EL bot está en funcionamiento')
    bot.infinity_polling() #bucle infinito donde se revisa si hay nuevos mensajes

