#!/usr/bin/env python
import pika
import json
import random
import datetime

startTime = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
currentTime = startTime

def publish(message):
    pvChannel = connection.channel()
    pvChannel.queue_declare(queue='hello')
    pvChannel.basic_publish(
        exchange='', routing_key='hello', body=json.dumps(message))

def nextMessage():
    global currentTime
    message = {
        "time": currentTime.strftime("%Y-%m-%d %H:%M:%S"),
        "pv": getPVFromTime()
    }
    currentTime += datetime.timedelta(minutes=5)
    return message

def getPVFromTime():
    if currentTime.hour < 6 or currentTime.hour >= 21:
        return 0

    x = (currentTime - startTime).total_seconds() / 60 / 60

    if currentTime.hour >= 6 and currentTime.hour < 8:
        return 125 * x - 750
    if currentTime.hour >= 20 and currentTime.hour < 21:
        return -150 * x + 3150

    return (-700 * x**2 / 9) + (19525 * x / 9) - (109150 / 9)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))    
# currentTime + inverval < ...
while currentTime < startTime + datetime.timedelta(days=1):
    publish(nextMessage())
publish(None)
connection.close()
