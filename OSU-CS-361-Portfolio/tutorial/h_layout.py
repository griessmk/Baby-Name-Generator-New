import sys

from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QLabel,
    QVBoxLayout
)

def h():
    print("h")

app = QApplication([])
window = QWidget()
window.setWindowTitle("QHBoxLayout")

layout = QHBoxLayout()
left_test = QPushButton("left Test")
left_test.clicked.connect(h)
layout.addWidget(left_test)
layout.addWidget(QPushButton("Center"))
layout.addWidget(QPushButton("Right"))
layout.addWidget(QLabel("<h1>Hello, World!</h1>"))
# window.setLayout(layout)
layout2 = QVBoxLayout()
layout2.addWidget(QPushButton("Left"))
layout2.addWidget(QPushButton("Center"))
layout2.addWidget(QPushButton("Right"))
layout2.addWidget(QLabel("<h1>Hello, World!</h1>"))
layout.addLayout(layout2)
window.setLayout(layout)

window.show()
sys.exit(app.exec())