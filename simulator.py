#!/usr/bin/env python
import pika
import pandas as pd
import plotly.express as px
import json
import datetime
import random

import plotly.graph_objects as go


class Simulator():
    startTime = datetime.datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0)
    modifier = 0
    timeList = []
    meterList = []
    pvList = []

    def __init__(self, queueName):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=queueName)
        channel.basic_consume(
            queue=queueName, on_message_callback=self.callback, auto_ack=True)
        # print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def getPVFromTime(self, currentTime):
        modifier = self.modifier

        # Before or after hours
        if currentTime.hour < 6 or currentTime.hour >= 21:
            return 0

        variability = 3000 * 0.010
        x = (currentTime - self.startTime).total_seconds() / 60 / 60
        y = (-700 * x**2 / 9) + (19525 * x / 9) - (109150 / 9)
        modifierModifer = random.uniform(variability * -1, variability)

        if modifier + modifierModifer > variability:
            modifier -= modifierModifer
        elif modifier - modifierModifer > variability:
            modifier += modifierModifer
        elif modifier + modifierModifer < -1 * variability:
            modifier -= modifierModifer
        elif modifier - modifierModifer < -1 * variability:
            modifier += modifierModifer
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
        return max(y + modifier, 0)

    def callback(self, ch, method, properties, body):
        messageDict = json.loads(body)
        if messageDict is not None:
            self.timeList.append(messageDict["time"])
            self.meterList.append(messageDict["consumption"])
            time = datetime.datetime.strptime(
                messageDict["time"], "%Y-%m-%d %H:%M:%S")
            self.pvList.append(self.getPVFromTime(time))
        else:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=self.timeList, y=self.meterList,
                                     fill='tozeroy', name="Consumption"))
            fig.add_trace(go.Scatter(x=self.timeList, y=self.pvList,
                                     fill='tozeroy', name="Generation"))
            fig.update_layout(
                title="Home Power",
                xaxis_title="Time",
                yaxis_title="Power (W)",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
            fig.show()

            self.timeList = []
            self.meterList = []

Simulator('default')
