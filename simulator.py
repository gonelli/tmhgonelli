#!/usr/bin/env python
import pika
import pandas as pd
import plotly.express as px
import json

def callback(ch, method, properties, body):
    # print(json.loads(body))
    # message = json.loads(body)

    df = pd.read_json(body)
    fig = px.area(df, x="time", y="PV")
    fig.show()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_consume(
    queue='hello', on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
