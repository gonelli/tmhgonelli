#!/usr/bin/env python
import pika
import json
import random

def publish(message):
    pvChannel = connection.channel()
    pvChannel.queue_declare(queue='hello')
    pvChannel.basic_publish(
        exchange='', routing_key='hello', body=json.dumps(message))

message = {
    "time": ["2015-02-17 12:00:01.23", "2015-02-17 12:00:02.23"],
    "PV": [random.randrange(0, 5, 1), random.randrange(0, 5, 1)]
}

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
publish(message)
connection.close()
