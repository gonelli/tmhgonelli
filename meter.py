#!/usr/bin/env python
import pika
import json
import random
import datetime

class Meter():
    startTime = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    currentTime = startTime
    connection = None
    channel = None
    queueName = 'default'
    timeDelta = 2
    relativeUsage = 1.0

    def __init__(self, queueName='default'):

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        self.queueName = queueName
        self.channel.queue_declare(queue=queueName)

    def publish(self, message):
        self.channel.basic_publish(
            exchange='', routing_key=self.queueName, body=json.dumps(message))

    def getConsptionFromTime(self):
        # https://www.desmos.com/calculator/sanlujpfmc
        # x is in hours
        x = (self.currentTime - self.startTime).total_seconds() / 60 / 60
        a = 0.25228
        b = -15.1446
        c = 256.716
        d = -932.24
        f = 3530.65
        y = a*x**4 + b*x**3 + c*x**2 + d*x + f

        return max(y, 0) / -1000 * self.relativeUsage

    def nextMessage(self):
        message = {
            "time": self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
            "consumption": self.getConsptionFromTime()
        }
        self.currentTime += datetime.timedelta(seconds=self.timeDelta)
        return message

    def start(self):
        while self.currentTime < self.startTime + datetime.timedelta(days=1):
            self.publish(self.nextMessage())
        self.publish(None)
        self.connection.close()


if __name__ == '__main__':
    Meter('default').start()
