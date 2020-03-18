#!/usr/bin/env python
import pika
import json
import random
import datetime

class Meter():
    startTime = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    currentTime = startTime
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    queueName = 'default'

    def __init__(self, queueName):
        self.queueName = queueName

    def publish(self, message):
        pvChannel = self.connection.channel()
        pvChannel.queue_declare(queue=self.queueName)
        pvChannel.basic_publish(exchange='', routing_key=self.queueName, body=json.dumps(message))

    def getConsumeFromTime(self):
        # https://www.desmos.com/calculator/sanlujpfmc
        x = (self.currentTime - self.startTime).total_seconds() / 60 / 60
        a = 0.25228
        b = -15.1446
        c = 256.716
        d = -932.24
        f = 3530.65
        y = a*x**4 + b*x**3 + c*x**2 + d*x + f

        return max(y, 0)

    def nextMessage(self):
        message = {
            "time": self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
            "consumption": self.getConsumeFromTime()
        }
        self.currentTime += datetime.timedelta(minutes=2)
        return message

    def start(self):
        # currentTime + inverval < ...
        print("Start")
        while self.currentTime < self.startTime + datetime.timedelta(days=1):
            self.publish(self.nextMessage())
        self.publish(None)
        self.connection.close()

Meter('default').start()
