#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: procesador_de_tiempo_de_medicamento.py
# Capitulo: 3 Estilo Publica-Subscribe
# Autor(es): Carlos Javier.
# Version: 1.0 Marzo 2021
# Descripción:
#
#   Esta clase define el rol de un suscriptor, es decir, es un componente que recibe mensajes.
#
#   Las características de ésta clase son las siguientes:
#
#                                     procesador_de_tiempo_de_medicamento.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |                         |  - Se suscribe a los   |
#           |                       |                         |    eventos generados   |
#           |                       |  - Procesar el tiempo   |    por el wearable     |
#           |     Procesador de     |    para determinar la   |    Xiaomi My Band.     |
#           |     tiempo de         |    prescripción del     |                        |         
#           |     medicamento       |    medicamento.         |  - Define la hora,     |
#           |                       |                         |    el medicamento y    |
#           |                       |                         |    la dosis para       |
#           |                       |                         |    prescripción.       |
#           |                       |                         |                        |
#           |                       |                         |                        |
#           +-----------------------+-------------------------+------------------------+
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                               Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Recibe las horas,  |
#           |       consume()        |          Ninguno         |    los medicamentos y |
#           |                        |                          |    la dosis para la   |
#           |                        |                          |    prescripción del   |
#           |                        |                          |    adulto mayor       |
#           |                        |                          |    desde el distribui-|
#           |                        |                          |    dor de mensajes.   |
#           +------------------------+--------------------------+-----------------------+
#           |                        |  - ch: propio de Rabbit. |  - Procesa y detecta  |
#           |                        |  - method: propio de     |    hora y medicamento |
#           |                        |     Rabbit.              |    que se debe de     |
#           |       callback()       |  - properties: propio de |    suministrar.       |
#           |                        |     Rabbit.              |                       |
#           |                        |  - body: mensaje recibi- |                       |
#           |                        |     do.                  |                       |
#           +------------------------+--------------------------+-----------------------+
#           |    string_to_json()    |  - string: texto a con-  |  - Convierte un string|
#           |                        |     vertir en JSON.      |    en un objeto JSON. |
#           +------------------------+--------------------------+-----------------------+
#
#
#           Nota: "propio de Rabbit" implica que se utilizan de manera interna para realizar
#            de manera correcta la recepcion de datos, para éste ejemplo no hubo necesidad
#            de utilizarlos y para evitar la sobrecarga de información se han omitido sus
#            detalles. Para más información acerca del funcionamiento interno de RabbitMQ
#            puedes visitar: https://www.rabbitmq.com/
#
#-------------------------------------------------------------------------

import pika
import sys
sys.path.append('../')
from monitor import Monitor
import time

class ProcesadorMedicamentos:

    def consume(self):
        try:
            # Se establece la conexión con el Distribuidor de Mensajes
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            # Se solicita un canal por el cuál se enviarán los signos vitales
            channel = connection.channel()
            # Se declara una cola para leer los mensajes enviados por el
            # Publicador
            channel.queue_declare(queue='medication_time', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(on_message_callback=self.callback, queue='medication_time')
            channel.start_consuming()  # Se realiza la suscripción en el Distribuidor de Mensajes
        except (KeyboardInterrupt, SystemExit):
            channel.close()  # Se cierra la conexión
            sys.exit("Conexión finalizada...")
            time.sleep(1)
            sys.exit("Programa terminado...")


    def callback(self, ch, method, properties, body):
        json_message = self.string_to_json(body)

        hour = int(json_message['hour'])
        minute = int(json_message['minute'])

        datetime = json_message['hour']+':'+json_message['minute']

        # Establecemos horas de suministro de medicamentos para los adultos
        if hour == 8 or hour == 16 or hour == 22:

            if minute == 0:

                monitor = Monitor()
                monitor.print_notification_dose(datetime, json_message['id'], json_message[
                    'medicine'], json_message['dose'], json_message['model'])

        time.sleep(1)
        ch.basic_ack(delivery_tag=method.delivery_tag)


    def string_to_json(self, string):
        message = {}
        string = string.decode('utf-8')
        string = string.replace('{', '')
        string = string.replace('}', '')
        values = string.split(', ')
        for x in values:
            v = x.split(': ')
            message[v[0].replace('\'', '')] = v[1].replace('\'', '')
        return message

if __name__ == '__main__':
    p_tiempo_medicamento = ProcesadorMedicamentos()
    p_tiempo_medicamento.consume()