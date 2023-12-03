import sys

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QComboBox
)

import qdarktheme

class ChoiceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        qdarktheme.setup_theme('light')

    def initUI(self):
        self.layout = QVBoxLayout()
        self.choices = ["Choice 1", "Choice 2", "Choice 3", "Choice 4", "Choice 5", "Choice 6", "Choice 7", "Choice 8", "Choice 9", "Choice 10"]
        self.selected_choices = []

        self.current_choice = 0

        self.label = QLabel("Select your choices:")

        self.choice_button = QPushButton("Start", self)
        self.choice_button.clicked.connect(self.showChoices)

        combo_box = QComboBox()
        combo_box.addItems(qdarktheme.get_themes())
        combo_box.currentTextChanged.connect(qdarktheme.setup_theme)

        self.layout.addWidget(combo_box)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.choice_button)

        self.setLayout(self.layout)

    def showChoices(self):
        if self.current_choice < 10:
            choice_1 = self.choices[self.current_choice]
            choice_2 = self.choices[self.current_choice + 1]

            if not self.choice_button.isHidden():
                self.layout.removeWidget(self.choice_button)  # Remove the "Start" button
                self.choice_button.hide()  # Delete the "Start" button widget
            else:
                self.layout.removeWidget(self.choice_1)
                self.layout.removeWidget(self.choice_2)
                self.layout.removeWidget(self.choice_1_button)
                self.layout.removeWidget(self.choice_2_button)

            self.choice_layout = QGridLayout()
            self.choice_1 = QLabel(choice_1)
            self.choice_2 = QLabel(choice_2)
            self.choice_1_button = QPushButton("Select", self)
            self.choice_2_button = QPushButton("Select", self)

            self.choice_layout.addWidget(self.choice_1, 0, 0)
            self.choice_layout.addWidget(self.choice_2, 0, 1)
            self.choice_layout.addWidget(self.choice_1_button, 1, 0)
            self.choice_layout.addWidget(self.choice_2_button, 1, 1)

            self.choice_1_button.clicked.connect(lambda checked, c=choice_1: self.selectChoice(c))
            self.choice_2_button.clicked.connect(lambda checked, c=choice_2: self.selectChoice(c))

            self.layout.addLayout(self.choice_layout)

            self.current_choice += 2
        else:
            self.layout.removeWidget(self.choice_1)
            self.layout.removeWidget(self.choice_2)
            self.layout.removeWidget(self.choice_1_button)
            self.layout.removeWidget(self.choice_2_button)
            self.choice_1.deleteLater()
            self.choice_2.deleteLater()
            self.choice_1_button.deleteLater()
            self.choice_2_button.deleteLater()
            self.layout.removeWidget(self.label)
            self.label.deleteLater()
            self.displaySelectedChoices()

    def selectChoice(self, choice):
        self.selected_choices.append(choice)
        self.showChoices()

    def displaySelectedChoices(self):
        self.layout.addWidget(QLabel("Selected Choices:"))
        for choice in self.selected_choices:
            self.layout.addWidget(QLabel(choice))


class StartScreen(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.layout = QGridLayout()
        self.dark_theme_button = QPushButton('')
        self.dark_theme_button.setIcon(QIcon('../img/moon.png'))
        self.dark_theme_button.setIconSize(QSize(25, 25))
        self.dark_theme_button.setFixedSize(40, 40)
        self.dark_theme_button.clicked.connect(main_window.toggle_dark_mode)
        self.choice_button = QPushButton("Start", self)
        self.choice_button.setFixedSize(100, 50)
        self.choice_button.clicked.connect(main_window.set_new_widget)

        self.layout.addWidget(self.dark_theme_button, 0, 0)
        self.layout.addWidget(self.choice_button, 1, 4)

        self.setLayout(self.layout)


class TestWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel("Select your choices:")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Baby Name Chooser!')
        self.setFixedSize(400, 300)
        self.central_widget = StartScreen(self)
        self.setCentralWidget(self.central_widget)
        self.current_theme = 'light'
        qdarktheme.setup_theme('light')

    def set_new_widget(self):
        self.central_widget = TestWidget()
        self.setCentralWidget(self.central_widget)

    def toggle_dark_mode(self):
        if self.current_theme == 'light':
            self.current_theme = 'dark'
            qdarktheme.setup_theme('dark')
        else:
            self.current_theme = 'light'
            qdarktheme.setup_theme('light')

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
