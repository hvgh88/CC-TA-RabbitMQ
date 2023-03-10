import pika
import pymongo
from pymongo import MongoClient
import json

def read_from_database():
    list_records = []
    conn_string = f'mongodb://mongo:27017/testDatabase'
    myclient = MongoClient(conn_string)
    db = myclient.testDatabase
    db_content = db["mini_project"]
    records = db_content.find()
    for record in records:
    	list_records.append(record)
    	print(record)

print(' Connecting to server ...')

connection = pika.BlockingConnection(pika.ConnectionParameters(host="172.22.0.1"))
channel = connection.channel()
channel.exchange_declare(exchange='direct_logs',exchange_type='direct')
queue=channel.queue_declare(queue='',durable=True)
channel.queue_bind(exchange='direct_logs',queue=queue.method.queue,routing_key='read_db')


print(' Waiting for messages...')


def callback(ch, method, properties, body):
    read_from_database()
    print("Read operation complete")

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue.method.queue, on_message_callback=callback)
channel.start_consuming()
