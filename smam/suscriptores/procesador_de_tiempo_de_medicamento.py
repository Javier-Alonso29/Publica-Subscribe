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