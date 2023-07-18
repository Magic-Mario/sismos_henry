from configuracion import * # el archivo configuración, recojo el token
import telebot # manejar la api de telegram
import requests #hacer las peticiones a las api
import schedule #hacer tareas para cumplir
import datetime as dt #modificar las fechas de la api gringa
import time



bot = telebot.TeleBot(token) #creo el bot

paises ={'usa':-906979202,'japan':-940924711,'chile':-905389283}

def informar_terremoto():
    for pais in paises.keys():
        # Realizar la solicitud GET a la API de la USGS
        consulta_pais = requests.get(f"https://henrypf-sismos-prueba.onrender.com/country/{pais}?latest=true")

        # Verificar el código de estado de la respuesta
        if consulta_pais.status_code == 200:

            # Mensaje en consola de la actividad hecha
            print(f'Datos obtenidos de {pais}')

            # Transformo la consulta en formato JSON
            datos = consulta_pais.json()


            # Verifico que sí hayan datos disponibles
            if datos:

                #Mensaje en consola de la activida hecha
                print(f' Extrayendo datos de {pais}')

                # Determino la fecha de la consulta
                tiempo = dt.datetime.strptime(datos['time'],"%Y-%m-%dT%H:%M:%S.%f")
                # Sustraigo la fecha de la consulta
                fecha = tiempo.strftime("%Y-%m-%d")
                
                print(f"la fecha de la consulta es {fecha}")

                # Determino la fecha actual
                tiempo_actual = dt.datetime.now()
                # sustraigo la fecha actual
                fecha_actual = tiempo_actual.strftime("%Y-%m-%d")
                
                print(f"la fecha actual es {fecha_actual}")
                
                # Verifico que los datos sean del mismo día a través de la fechas sacadas anteriormente
                if fecha == fecha_actual:

                    #Mensaje en consola de la activida hecha
                    print( f'Se confirma terremoto el mismo día en  {pais}')

                    # Determino la hora de la consulta
                    hora = tiempo.time()
                    
                    print(f"la hora de la consulta es {hora}")

                    
                    # Determino la hora de actual
                    hora_actual = tiempo_actual.time()
                    
                    print(f"la hora actual es {hora_actual}")


                    # Calculo la diferencia entre horas
                    diferencia = (dt.datetime.combine(dt.date.min, hora_actual) - dt.datetime.combine(dt.date.min, hora))
                    
                    print(f"la diferencia entre hora actual y hora de la consulta es {diferencia}")

                    # Determino el valor de una hora 
                    una_hora = dt.timedelta(hours=1/30)

                    # Se determina si el evento sismico sucedio hace una hora o menos
                    if diferencia.seconds <= una_hora.total_seconds():

                        #Consulto la predicción del modelo
                        consulta_clasificacion = requests.get(f"https://henrypf-sismos-prueba.onrender.com/classf?depth={datos['depth']}&magnitude={datos['mag']}")
                        #Convierto la consulta en json
                        datos_clasificacion = consulta_clasificacion.json()

                        #Creo el mensaje para mandar por el bot
                        mensaje = f"Se identifico un terremoto a las {hora}.\n- Magnitud de {datos['mag']}\n- Profundidad de {datos['depth']} km.\n- Lugar {datos['place']}.\n- Clasificación: {datos_clasificacion['classification'][0]}\n- Observación: {datos_clasificacion['alert']}  "
                        bot.send_message(paises[pais], mensaje)
                    else:
                        # Mensajes en caso de que el evento no haya sucedido en un rango de una hora
                        print(f'No ha habido evento en {pais} en un rango de una hora')
                else:
                    # Mensaje en consola en caso de que los datos no seán del mismo día
                    print(f'Los datos de {pais} no son del mismo día')
            else:
                # Mensaje en consola en caso de que no se hayan encontrado datos
                print(f'No se encontraron datos de {pais}')
        else:
            #mensaje de error por si la consulta no funcionó
            print("Error al realizar la solicitud:", consulta_pais.status_code)


schedule.every(2).minutes.do(informar_terremoto)
while True:
    schedule.run_pending()
    time.sleep(5)

    
