import sys

from PyQt6.QtWidgets import QApplication, QLabel, QWidget

app = QApplication([])
window = QWidget()
window.setWindowTitle("Test App")
window.setGeometry(500, 500, 400, 500)
msg = QLabel("<h1>Hello, World!</h1>", parent=window)
msg.move(100, 150)

window.show()
sys.exit(app.exec())
