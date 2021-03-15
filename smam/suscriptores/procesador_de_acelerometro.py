#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: procesador_de_acelerometro.py
# Capitulo: 3 Estilo Publica-Subscribe
# Autor(es): Miguel Valadez.
# Version: 1.0 Marzo 2021
# Descripción:
#
#   Esta clase define el rol de un suscriptor, es decir, es un componente que recibe mensajes.
#
#   Las características de ésta clase son las siguientes:
#
#                                     procesador_de_acelerometro.py
#           +-----------------------+-------------------------+------------------------+
#           |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#           +-----------------------+-------------------------+------------------------+
#           |                       |                         |  - Se suscribe a los   |
#           |                       |                         |    eventos generados   |
#           |                       |  - Procesar valores     |    por el wearable     |
#           |     Procesador de     |    irregulares de la    |    Xiaomi My Band.     |
#           |      acelerometro     |    las coordenadas      |  - Define el valor     |
#           |                       |    haciendo enfasis     |    del eje z para      |
#           |                       |    en la coordenada z   |    detectar una caida. |
#           |                       |    para determinar si   |  - Notifica al monitor |
#           |                       |    alguien se cayó.     |    cuando se cayó un   |
#           |                       |                         |    paciente.           |
#           +-----------------------+-------------------------+------------------------+
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                               Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Recibe las coorde- |
#           |       consume()        |          Ninguno         |    nadas del wearable |
#           |                        |                          |    desde el distribui-|
#           |                        |                          |    dor de mensajes.   |
#           +------------------------+--------------------------+-----------------------+
#           |                        |  - ch: propio de Rabbit. |  - Procesa y detecta  |
#           |                        |  - method: propio de     |    irregularidades en |
#           |                        |     Rabbit.              |    el eje z para de-  |
#           |       callback()       |  - properties: propio de |    terminar una caida.|
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

class ProcesadorCoordenadas:

    def consume(self):
        try:
        # Se establece la conexión con el Distribuidor de Mensajes
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            # Se solicita un canal por el cuál se enviarán los signos vitales
            channel = connection.channel()
            # Se declara una cola para leer los mensajes enviados por el
            # Publicador
            channel.queue_declare(queue='coordenada', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(on_message_callback=self.callback, queue='coordenada')
            channel.start_consuming() #Se realiza la suscripción en el Distribuidor de Mensajes
        except (KeyboardInterrupt, SystemExit):
            channel.close() #Se cierra la conexión
            sys.exit("Conexión finalizada...")
            time.sleep(1)
            sys.exit("Programa terminado...")
        
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
    
    def callback(self, ch, method, properties, body):
        json_message = self.string_to_json(body)
        if  float(json_message['coordenada_z']) < 0.40: #Se evalúa que la coordenada este debajo de la norma
            monitor = Monitor()
            monitor.print_notification_cordinate(json_message['datetime'], json_message['id'], json_message['coordenada_x'],
                                                json_message['coordenada_y'], json_message['model'], 'caida')
        time.sleep(1)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
if __name__=='__main__':
    p_acelerometro = ProcesadorCoordenadas()
    p_acelerometro.consume()
