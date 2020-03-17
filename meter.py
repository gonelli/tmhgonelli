#!/usr/bin/env python
import pika
import json
import random
import datetime

currentDate = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
currentTime = currentDate

def publish(message):
    pvChannel = connection.channel()
    pvChannel.queue_declare(queue='hello')
    pvChannel.basic_publish(
        exchange='', routing_key='hello', body=json.dumps(message))

def nextMessage():
    global currentTime
    # print(currentTime.strftime("%Y-%m-%d %H:%M:%S"))

    message = {
        "time": currentTime.strftime("%Y-%m-%d %H:%M:%S"),
        "pv": random.randrange(0, 15, 1)
    }

    currentTime += datetime.timedelta(minutes=1)

    return message

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))    
while currentTime < currentDate + datetime.timedelta(days=1): #currentTime + inverval < ...
    publish(nextMessage())
publish(None)
connection.close()
