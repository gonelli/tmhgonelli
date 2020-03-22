# tmhgonelli
TMH's PV Simulator

## Setup ##
Must install and start RabbitMQ Server to run this application

```
$ rabbitmq-server
```

Use pip to install all of the required packages

## Running via GUI ##
To run the application with GUI options, run:

```
$ python tmhgonelli.py
```

Adjust the parameters 

## Running via CLI only ##
To run the application in its original form, run:

```
$ python simulator.py
```

This will start consuming all data passed to the broker. In a separate window, run:

```
$ python meter.py
```

This will send home comsumption data to be received and logged by the simulator
