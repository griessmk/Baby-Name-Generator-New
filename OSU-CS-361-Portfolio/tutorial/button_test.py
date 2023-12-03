import sys
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("Comprehensive PyQt5 Button Guide")
        pybutton = QPushButton('Click me', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(100,320)
        pybutton.move(50, 50)
    def clickMethod(self):
        print('Button pressed in PyQt application.')
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())