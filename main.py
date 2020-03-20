import sys
import threading
import multiprocessing
from simulator import Simulator
from meter import Meter
from PyQt5 import QtCore, QtGui, QtWidgets, uic

class MyApp(QtWidgets.QMainWindow):
    simulatorProcess = None
    mySim = None

    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('config.ui', self)
        self.simulateButton.clicked.connect(self.sendMeter)
        self.brokerButton.clicked.connect(self.toggleBroker)
        self.setNthSlider()
        self.setIntensitySlider()
        self.setTimeSlider()
        self.setConsumptionSlider()
        self.simulateButton.setEnabled(False)

    def setIntensitySlider(self):
        self.intensitySlider.setMinimum(1)
        self.intensitySlider.setMaximum(10)
        self.intensitySlider.setValue(2)
        self.intensitySlider.setTickInterval(1)
        self.intensitySlider.valueChanged.connect(self.changedIntensitySlider)
        self.intensityValueLabel.setText(str(self.intensitySlider.value()) + " pts.")

    def setTimeSlider(self):
        self.timeSlider.setMinimum(1)
        self.timeSlider.setMaximum(10)
        self.timeSlider.setValue(2)
        self.timeSlider.setTickInterval(1)
        self.timeSlider.valueChanged.connect(self.changedTimeSlider)
        self.timeValueLabel.setText(str(self.timeSlider.value()) + " pts.")
        
    def setConsumptionSlider(self):
        self.consumptionSlider.setMinimum(1)
        self.consumptionSlider.setMaximum(10)
        self.consumptionSlider.setValue(2)
        self.consumptionSlider.setTickInterval(1)
        self.consumptionSlider.valueChanged.connect(self.changedConsumptionSlider)
        self.consumptionValueLabel.setText(str(self.consumptionSlider.value()) + " pts.")

    def setNthSlider(self):
        self.nthSlider.setMinimum(60)
        self.nthSlider.setMaximum(1200)
        self.nthSlider.setValue(60)
        self.nthSlider.setTickInterval(1)
        self.nthSlider.valueChanged.connect(self.changedNthSlider)
        self.nthValueLabel.setText(str(self.nthSlider.value()) + " pts.")

    def changedNthSlider(self):
        self.nthValueLabel.setText(str(self.nthSlider.value()) + " pts.")
        if self.brokerButton.text() == "Stop Broker":
            self.toggleBroker()

    def changedTimeSlider(self):
        self.timeValueLabel.setText(str(self.timeSlider.value()) + " pts.")

    def changedIntensitySlider(self):
        self.intensityValueLabel.setText(str(self.intensitySlider.value()) + " pts.")

    def changedConsumptionSlider(self):
        self.consumptionValueLabel.setText(str(self.consumptionSlider.value()) + " pts.")

    def toggleBroker(self):
        # Broker is running, so stop it
        if self.brokerButton.text() == "Stop Broker":
            # self.brokerButton.setCheckable(False)
            self.simulateButton.setEnabled(False)
            self.simulatorProcess.terminate()
            self.brokerButton.setText("Start Broker")
        # Broker is stopped, so start it
        else:
            # self.brokerButton.setCheckable(True)
            self.simulateButton.setEnabled(True)
            self.mySim = Simulator()
            self.mySim.n = self.nthSlider.value()
            self.simulatorProcess = multiprocessing.Process(
                target=self.mySim.startConsuming)
            self.simulatorProcess.daemon = True
            self.simulatorProcess.start()
            self.simulatorProcess.join(0)
            self.brokerButton.setText("Stop Broker")

    def sendMeter(self):
        meter = Meter()
        meter.timeDelta = self.timeSlider.value()
        meter.start()
        print("Button!")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
