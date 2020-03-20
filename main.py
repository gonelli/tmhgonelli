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
        self.openCSVBox.clicked.connect(self.boxToggled)
        self.createGraphBox.clicked.connect(self.boxToggled)
        self.setNthSlider()
        self.setIntensitySlider()
        self.setTimeSlider()
        self.setConsumptionSlider()

        if sys.platform == "win32":
            self.openCSVBox.setParent(None)

    def boxToggled(self):
        if self.brokerButton.text() == "Stop Broker":
            self.toggleBroker()

    def setIntensitySlider(self):
        self.intensitySlider.setMinimum(0)
        self.intensitySlider.setMaximum(200)
        self.intensitySlider.setValue(100)
        self.intensitySlider.setTickInterval(1)
        self.intensitySlider.valueChanged.connect(self.changedIntensitySlider)
        self.intensityValueLabel.setText(str(self.intensitySlider.value()) + "%")

    def setTimeSlider(self):
        self.timeSlider.setMinimum(1)
        self.timeSlider.setMaximum(10)
        self.timeSlider.setValue(2)
        self.timeSlider.setTickInterval(1)
        self.timeSlider.valueChanged.connect(self.changedTimeSlider)
        self.timeValueLabel.setText(str(self.timeSlider.value()) + " sec.")
        
    def setConsumptionSlider(self):
        self.consumptionSlider.setMinimum(0)
        self.consumptionSlider.setMaximum(200)
        self.consumptionSlider.setValue(100)
        self.consumptionSlider.setTickInterval(1)
        self.consumptionSlider.valueChanged.connect(self.changedConsumptionSlider)
        self.consumptionValueLabel.setText(str(self.consumptionSlider.value()) + "%")

    def setNthSlider(self):
        self.nthSlider.setMinimum(1)
        self.nthSlider.setMaximum(1000)
        self.nthSlider.setValue(60)
        self.nthSlider.setTickInterval(1)
        self.nthSlider.valueChanged.connect(self.changedNthSlider)
        self.nthValueLabel.setText(str(self.nthSlider.value()) + " pts.")

    def changedIntensitySlider(self):
        self.intensityValueLabel.setText(str(self.intensitySlider.value()) + "%")
        if self.brokerButton.text() == "Stop Broker":
            self.toggleBroker()

    def changedTimeSlider(self):
        self.timeValueLabel.setText(str(self.timeSlider.value()) + " pts.")

    def changedConsumptionSlider(self):
        self.consumptionValueLabel.setText(str(self.consumptionSlider.value()) + "%")

    def changedNthSlider(self):
        self.nthValueLabel.setText(str(self.nthSlider.value()) + " pts.")
        if self.brokerButton.text() == "Stop Broker":
            self.toggleBroker()

    def toggleBroker(self):
        # Broker is running, so stop it
        if self.brokerButton.text() == "Stop Broker":
            self.simulateButton.setEnabled(False)
            self.simulatorProcess.terminate()
            self.brokerButton.setText("Start Broker")
        # Broker is stopped, so start it
        else:
            self.simulateButton.setEnabled(True)
            self.mySim = Simulator()
            self.mySim.n = self.nthSlider.value()
            self.mySim.intensity = float(self.intensitySlider.value()) / 100.0
            self.mySim.openCSV = self.openCSVBox.isChecked()
            self.mySim.createGraph = self.createGraphBox.isChecked()
            self.simulatorProcess = multiprocessing.Process(
                target=self.mySim.startConsuming)
            self.simulatorProcess.daemon = True
            self.simulatorProcess.start()
            self.simulatorProcess.join(0)
            self.brokerButton.setText("Stop Broker")

    def sendMeter(self):
        meter = Meter()
        meter.timeDelta = self.timeSlider.value()
        meter.relativeUsage = float(self.consumptionSlider.value()) / 100.0
        meter.start()
        print("Button!")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
