#!/usr/bin/env python
import pika
import pandas as pd
import plotly.express as px
import json
import csv
import datetime
import random
import threading

import plotly.graph_objects as go


class Simulator():
    modifier = 0
    timeList = []
    meterList = []
    pvList = []
    netPowerList = []

    n = 60

    connection = None
    channel = None

    def __init__(self):
        # print(' [*] Waiting for messages. To exit press CTRL+C')
        pass

    def startConsuming(self, queueName='default'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queueName)
        self.channel.basic_consume(
            queue=queueName, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()
    
    def stopConsuming(self):
        if self.channel is not None:
            self.channel.stop_consuming()

    def getPVFromTime(self, currentTime):
        modifier = self.modifier

        # Before or after hours
        if currentTime.hour < 6 or currentTime.hour >= 21:
            return 0

        variability = 3000 * 0.015
        startTime = currentTime.replace(
            hour=0, minute=0, second=0, microsecond=0)
        x = (currentTime - startTime).total_seconds() / 60 / 60
        y = (-700 * x**2 / 9) + (19525 * x / 9) - (109150 / 9)
        modifierModifer = random.uniform(variability * -1, variability)

        if abs(modifier + modifierModifer) > abs(variability):
            modifier -= modifierModifer
        else:
            modifier += modifierModifer

        # Startup hours
        if currentTime.hour >= 6 and currentTime.hour < 8:
            y = 125 * x - 750

        # Wind down hours
        if currentTime.hour >= 20 and currentTime.hour < 21:
            y = -150 * x + 3150

        self.modifier = modifier
        self.currentTime = currentTime
        return max(y + modifier, 0) / 1000

    def callback(self, ch, method, properties, body):
        messageDict = json.loads(body)
        if messageDict is not None:
            self.timeList.append(messageDict["time"])
            self.meterList.append(messageDict["consumption"])
            
            currentTime = datetime.datetime.strptime(
                messageDict["time"], "%Y-%m-%d %H:%M:%S")
            pvGenerated = self.getPVFromTime(currentTime)
            self.pvList.append(pvGenerated)
            self.netPowerList.append(pvGenerated + messageDict["consumption"])
        else:
            n = self.n
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=self.timeList[::n], y=self.meterList[::n],
                                     fill='tozeroy', name="Consumption"))
            fig.add_trace(go.Scatter(x=self.timeList[::n], y=self.pvList[::n],
                                     fill='tozeroy', name="Generation"))
            fig.add_trace(go.Scatter(x=self.timeList[::n], y=self.netPowerList[::n],
                                     fill='tozeroy', name="Net Power"))
            fig.update_layout(
                title="Home Power",
                xaxis_title="Time",
                yaxis_title="Power (kW)",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
            fig.show()

            # a = zip(self.timeList, self.meterList, self.pvList, self.netPowerList)
            # with open("output.csv", "w", newline="") as f:
            #     writer = csv.writer(f)
            #     writer.writerows(a)

            self.timeList = []
            self.meterList = []
            self.pvList = []
            self.netPowerList = []
            self.modifier = 0

if __name__ == '__main__':
    sim = Simulator()
    sim.startConsuming('default')
    sim.startConsuming()
