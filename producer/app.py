from flask import Flask, request
import pika
import pymongo
from pymongo import MongoClient
import json

app = Flask(__name__)


@app.route('/')
def index():
    return 'Flask App Running'
    
@app.route('/delete_all')
def delete_all_records():
	conn_string = f'mongodb://mongo:27017/testDatabase'
	myclient = MongoClient(conn_string)
	db = myclient.testDatabase
	db_content = db["mini_project"]
	db_content.delete_many({})
	return "All records deleted"
	
@app.route('/read_db')
def read_database():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="172.22.0.1"))
    channel = connection.channel()
    channel.exchange_declare(exchange="direct_logs",exchange_type="direct")
    channel.basic_publish(exchange="direct_logs", routing_key='read_db',body=test_cmd,properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    connection.close()
    return "__Read DB Complete"


@app.route('/health_check/<test_cmd>')
def add_one(test_cmd):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="172.22.0.1"))
    channel = connection.channel()
    channel.exchange_declare(exchange="direct_logs",exchange_type="direct")
    channel.basic_publish(exchange="direct_logs", routing_key='health_check',body=test_cmd,properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

   
    connection.close()
    return " ___ Message Sent: %s" % cmd


@app.route('/insert',methods=['POST'])
def add_two():
    message = {}
    print(request.args)
    message['Name'] = request.args.get('Name')
    message['SRN'] = request.args.get('SRN')
    message['Section'] = request.args.get('Section')
    print(message)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="172.22.0.1"))
    channel = connection.channel()
    channel.exchange_declare(exchange="direct_logs",exchange_type="direct")
    channel.basic_publish(
        exchange='direct_logs',
        routing_key='insert_record',
        body = json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
   
    connection.close()
    return " Added to DB : %s" % message['Name']

@app.route('/delete/<srn>')
def delete_record(srn):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="172.22.0.1"))
    channel = connection.channel()
    channel.exchange_declare(exchange="direct_logs",exchange_type="direct")
    #channel.queue_declare(queue='task_queue_three', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='delete_record',
        body=srn,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE  # make message persistent
        ))
   
    connection.close()
    return " Deleted: %s" % srn



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
