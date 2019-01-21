import pika
from database import database
import datetime

# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
credentials = pika.PlainCredentials('tmylmz', 'Taha2010')
parameters = pika.ConnectionParameters('192.168.1.21', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='airTest')


def callback(ch, method, properties, body):
    # print(" [x] Received %r" % body)
    database().insert_value('AMQP', datetime.datetime.now(), str(body))

def main():
    channel.basic_consume(callback,
                          queue='airTest',
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()