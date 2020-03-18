import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('config.ui', self)
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
