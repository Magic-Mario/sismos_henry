from configuracion import *
import telebot # manejar la api de telegram
from telebot.types import ReplyKeyboardMarkup #crear los botones
from telegram.ext import Application, ApplicationBuilder, ContextTypes, CommandHandler, Job, JobQueue, Updater #creacion de respuestas, mandar mensajes, 


bot = telebot.TeleBot(token) #creo el bot


@bot.message_handler(commands=['start','ayuda','estoy en peligro'])
def comando_start(mensaje):
    """muestra los comando disponibles"""
    bot.send_message(mensaje.chat.id, " Hola")

if __name__ == '__main__':
    print( 'EL bot está en funcionamiento')
    
    bot.infinity_polling() #bucle infinito donde se revisa si hay nuevos mensajes