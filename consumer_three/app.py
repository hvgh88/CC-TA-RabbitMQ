import pika
import pymongo
from pymongo import MongoClient
import json

def delete_from_database(message):
    print(message)
    conn_string = f'mongodb://mongo:27017/testDatabase'
    myclient = MongoClient(conn_string)
    db = myclient.testDatabase
    db.mini_project.delete_one({'SRN':message})
    print("Deleted record from database")

print(' Connecting to server ...')

connection = pika.BlockingConnection(pika.ConnectionParameters(host="172.22.0.1"))
channel = connection.channel()
channel.exchange_declare(exchange='direct_logs',exchange_type='direct')
queue=channel.queue_declare(queue='',durable=True)
channel.queue_bind(exchange='direct_logs',queue=queue.method.queue,routing_key='delete_record')


print(' Waiting for messages...')


def callback(ch, method, properties, body):
    print(" Received %s" % body.decode())
    delete_from_database(body.decode())
    print("Delete operation complete")

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue.method.queue, on_message_callback=callback)
channel.start_consuming()
