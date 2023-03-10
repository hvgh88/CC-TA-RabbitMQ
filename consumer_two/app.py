import pika
import pymongo
from pymongo import MongoClient
import json

def insert_into_database(message):
    print(message)
    conn_string = f'mongodb://mongo:27017/testDatabase'
    myclient = MongoClient(conn_string)
    db = myclient.testDatabase
    db.mini_project.insert_one(message)	
    print("Inserted into database")

print(' Connecting to server ...')

connection = pika.BlockingConnection(pika.ConnectionParameters(host="172.22.0.1"))
channel = connection.channel()
channel.exchange_declare(exchange='direct_logs',exchange_type='direct')
queue = channel.queue_declare(queue='', durable=True)
channel.queue_bind(exchange='direct_logs',queue=queue.method.queue,routing_key='task_two')

print(' Waiting for messages...')


def callback(ch, method, properties, body):
    print(" Received %s" % json.loads(body))
    insert_into_database(json.loads(body))
    print(" Done")

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue.method.queue, on_message_callback=callback)
channel.start_consuming()
