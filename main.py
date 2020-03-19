import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('config.ui', self)
        self.simulateButton.clicked.connect(self.simulate)
        # self.brokerButton.setCheckable(True)
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

    def setTimeSlider(self):
        self.timeSlider.setMinimum(1)
        self.timeSlider.setMaximum(10)
        self.timeSlider.setValue(2)
        self.timeSlider.setTickInterval(1)
        self.timeSlider.valueChanged.connect(self.changedTimeSlider)
        
    def setConsumptionSlider(self):
        self.consumptionSlider.setMinimum(1)
        self.consumptionSlider.setMaximum(10)
        self.consumptionSlider.setValue(2)
        self.consumptionSlider.setTickInterval(1)
        self.consumptionSlider.valueChanged.connect(
            self.changedConsumptionSlider)

    def setNthSlider(self):
        self.nthSlider.setMinimum(1)
        self.nthSlider.setMaximum(10)
        self.nthSlider.setValue(2)
        self.nthSlider.setTickInterval(1)
        self.nthSlider.valueChanged.connect(self.changedNthSlider)

    def changedNthSlider(self):
        self.nthValueLabel.setText(str(self.nthSlider.value()) + " pts.")

    def changedTimeSlider(self):
        self.timeValueLabel.setText(str(self.timeSlider.value()) + " pts.")

    def changedIntensitySlider(self):
        self.intensityValueLabel.setText(str(self.intensitySlider.value()) + " pts.")

    def changedConsumptionSlider(self):
        self.consumptionValueLabel.setText(str(self.consumptionSlider.value()) + " pts.")

    def toggleBroker(self):
        if self.brokerButton.isChecked():
            self.brokerButton.setCheckable(False)
            self.brokerButton.setText("Start Broker")
        else:
            self.brokerButton.setCheckable(True)
            self.brokerButton.setText("Stop Broker")
    def simulate(self):
        # price = int(self.price_box.toPlainText())
        # tax = (self.tax_rate.value())
        # total_price = price + ((tax / 100) * price)
        # total_price_string = "The total price with tax is: " + str(total_price)
        # self.results_window.setText(total_price_string)
        print("Button!")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
