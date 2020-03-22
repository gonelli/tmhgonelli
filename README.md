# tmhgonelli
TMH's PV Simulator

## Setup ##
The following assumes you have **Python3** and **pip** installed.
Install the required python packages:
```
$ pip3 install pika
$ pip3 install pandas
$ pip3 install plotly
```
Then install [RabbitMQ Server](https://www.rabbitmq.com/install-debian.html)
```
$ sudo apt install rabbitmq-server
```
And ensure the server is running
```
$ sudo rabbitmq-server
```

## Run ##
**Note**: please leave only one instance of the simulator (GUI or terminal) running at a time

### Via GUI ###
The GUI requires the following additional installation:
```
$ pip3 install PyQt5
```
Launch the GUI by running the following script:
```
$ python3 tmhgonelli.py
```
Adjust the parameters to your specification
* Time Delta: The time interval between each datapoint throughout the day
* Solar Intensity: Arbitrarily scales the PV power generated
* Plot Every N Points: Skip every N data points when plotting the graph
* Power Consumption: Arbitrarily scales the home power consumed

Start the simulator and then simulate the data. The results will be written in the repository to output.csv, and the graph may be launched in your browser.

**Note**: It may take a few seconds to generate all of the data if a low time delta is set

### Via CLI only ###
If you encounter issues with the GUI, you can instead run the producer and consumer files separately via CLI. To start the consumer:
```
$ python3 simulator.py
```
And in a separate window, you can run the producer:
```
$ python3 meter.py
```
The results will be written in the repository to output.csv, and the graph will be launched in your browser.

## Troubleshoot: ##
If you encounter issues plotting the graph (such as overlapping data): ensure that only one simulator instance is running (GUI or terminal), try restarting the simulator and/or the RabbitMQ server.

If the graph will not launch many seconds after pressing *Simulate* in the GUI, try stopping and restarting the simulator by toggling the other button.
