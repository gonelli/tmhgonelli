#!/usr/bin/env python
import pika
import pandas as pd
import plotly.express as px
import json

timeList = []
pvList = []

def callback(ch, method, properties, body):
    global timeList
    global pvList

    messageDict = json.loads(body)
    if messageDict is None:
        df = pd.read_json(json.dumps({"Time": timeList, "PV": pvList}))
        fig = px.area(df, x="Time", y="PV")
        fig.show()
        timeList = []
        pvList = []
        return

    timeList.append(messageDict["time"])
    pvList.append(messageDict["pv"])


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_consume(
    queue='hello', on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
