import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Main Window')

        settings_button = QPushButton('Settings', self)
        settings_button.clicked.connect(self.showSettings)

    def showSettings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 300, 200)
        self.setWindowTitle('Settings')

        layout = QVBoxLayout()
        ok_button = QPushButton('OK')
        cancel_button = QPushButton('Cancel')

        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())