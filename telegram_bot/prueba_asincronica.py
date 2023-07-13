import asyncio
from aiogram import Bot, types
from aiogram.utils import executor
import schedule

# Inicializar el bot
bot = Bot(token='TU_TOKEN_DEL_BOT')

# Función para enviar mensajes
async def enviar_mensaje():
    await bot.send_message(chat_id='ID_DEL_CHAT', text='Este es un mensaje programado')

# Función para programar tareas
def programar_tareas():
    schedule.every(5).seconds.do(asyncio.run, enviar_mensaje())

# Función para ejecutar el ciclo de tareas programadas
async def ejecutar_tareas_programadas():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

# Función para manejar comandos /start
async def iniciar_comando(message: types.Message):
    await message.reply("¡Hola! Bot en funcionamiento.")

# Configurar el manejador de comandos /start
dp = Dispatcher(bot)
dp.register_message_handler(iniciar_comando, commands=['start'])

# Ejecutar el bot y el ciclo de tareas programadas
async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(ejecutar_tareas_programadas())
    await executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())