import random
import sys
import requests
import json
import os

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QComboBox
)
import qdarktheme

from text import (
    home_screen_info,
    config_screen_info,
    whats_new_screen,
    picker_instructions,
    end_screen,
)
from boy_names import boy_names
from girl_names import girl_names
from neutral_names import neutral_names

# TODO Bracket


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Baby Name Picker!')
        self.setFixedSize(800, 600)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        # Layouts
        self.permanent_layout = QVBoxLayout(self.central_widget)
        self.button_layout = QHBoxLayout()
        self.main_screen_layout = QVBoxLayout()
        self.config_layout = QGridLayout()
        self.picker_layout = QGridLayout()
        self.end_screen_layout = QGridLayout()
        # Button layout
        self.dark_theme_button = QPushButton('')
        self.info_button = QPushButton('')
        self._add_button_widgets()
        # Home Screen
        self._build_home_screen_layout()
        # Alignments
        self.permanent_layout.addLayout(self.button_layout)
        self.permanent_layout.addLayout(self.main_screen_layout)
        self.permanent_layout.setAlignment(self.main_screen_layout, Qt.AlignmentFlag.AlignCenter)
        self.permanent_layout.setAlignment(self.button_layout, Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.permanent_layout)
        # Other
        self.current_theme = 'light'
        qdarktheme.setup_theme('light')
        self.config_selections = {
            'gender': '',
            'num_choices': 0,
            'source': ''
        }
        self.name_bank = []
        self.cur_name_stack = []
        self.cur_names = None
        self.manual_text = None

    def _add_button_widgets(self):

        self.dark_theme_button.setIcon(QIcon('./img/moon.png'))
        self.dark_theme_button.setIconSize(QSize(25, 25))
        self.dark_theme_button.setFixedSize(40, 40)
        self.dark_theme_button.clicked.connect(self._toggle_dark_mode)
        self.info_button.setIcon((QIcon('./img/info.png')))
        self.info_button.setIconSize(QSize(25, 25))
        self.info_button.setFixedSize(40, 40)
        self.button_layout.addWidget(self.dark_theme_button)
        self.button_layout.addWidget(self.info_button)

        return

    def _toggle_dark_mode(self):
        if self.current_theme == 'light':
            self.current_theme = 'dark'
            self.dark_theme_button.setIcon(QIcon('./img/moon_inverted.png'))
            self.info_button.setIcon(QIcon('./img/info_inverted.png'))
            qdarktheme.setup_theme('dark')
        else:
            self.current_theme = 'light'
            self.dark_theme_button.setIcon(QIcon('./img/moon.png'))
            self.info_button.setIcon((QIcon('./img/info.png')))
            qdarktheme.setup_theme('light')

    def _transition_to_config(self):
        self._clear_layout(self.main_screen_layout)

        instructions = QLabel(
            'Please adjust the settings and press "Ok." Click the "i" icon for additional information.')
        font = instructions.font()
        font.setPointSize(14)
        instructions.setFont(font)
        self.main_screen_layout.addWidget(instructions, alignment=Qt.AlignmentFlag.AlignCenter)

        gender_label = QLabel('Gender')
        self.gender_dropdown = QComboBox()
        self.gender_dropdown.addItems(['Both', 'Boy', 'Girl', 'Neutral'])

        num_choices_label = QLabel('Size of Name Pool')
        self.num_choices_drowdown = QComboBox()
        self.num_choices_drowdown.addItems(['2', '4', '8', '16', '32', '64', '128', '256'])

        name_source_label = QLabel('Name Source')
        self.name_source_drowdown = QComboBox()
        self.name_source_drowdown.addItems(['Random', 'Top 1000', 'Manual'])

        ok_button = QPushButton('Ok')
        ok_button.setFixedSize(60, 30)
        ok_button.clicked.connect(self._transition_picker_from_config)

        cancel_button = QPushButton('Cancel')
        cancel_button.setFixedSize(60, 30)
        cancel_button.clicked.connect(lambda x: self._return_to_home_screen(self.config_layout, self.main_screen_layout))

        self.config_layout.addWidget(gender_label, 0, 0)
        self.config_layout.addWidget(self.gender_dropdown, 0, 1)
        self.config_layout.addWidget(num_choices_label, 1, 0)
        self.config_layout.addWidget(self.num_choices_drowdown, 1, 1)
        self.config_layout.addWidget(name_source_label, 2, 0)
        self.config_layout.addWidget(self.name_source_drowdown, 2, 1)
        self.config_layout.addWidget(ok_button, 3, 0)
        self.config_layout.addWidget(cancel_button, 3, 1)

        self.permanent_layout.addLayout(self.config_layout)
        self.permanent_layout.setAlignment(self.config_layout, Qt.AlignmentFlag.AlignCenter)

        self._reconfigure_info_button(config_screen_info, 'Config', 13)

    def _reconfigure_info_button(self, text, title, font_size):
        try:
            self.info_button.disconnect()
        except TypeError:  # Button has nothing connected to it.
            pass
        try:
            self.dark_theme_button.disconnect()
        except TypeError:
            pass
        self.info_button.clicked.connect(lambda x: self.display_info(text, title, font_size))
        self.dark_theme_button.clicked.connect(self._toggle_dark_mode)

    def _return_to_home_screen(self, *args):
        for layout in args:
            self._clear_layout(layout)
        self._clear_names()
        self._build_home_screen_layout()

    def _transition_picker_from_config(self):
        self._populate_config_selections()
        self._populate_name_bank()
        if not self.name_bank:
            return
        self._populate_name_stack()
        self._clear_layout(self.config_layout)
        self._clear_layout(self.main_screen_layout)

        bracket_button = QPushButton("Show Bracket")
        bracket_button.setFixedSize(100, 30)
        bracket_button.clicked.connect(self._show_bracket)

        self.names_remaining = QLabel(f'Names remaining: {len(self.name_bank)}')
        font = self.names_remaining.font()
        font.setPointSize(12)
        self.names_remaining.setFont(font)
        selection_question = QLabel("Which name do you prefer?")
        selection_question.setMinimumSize(200, 30)
        font = selection_question.font()
        font.setPointSize(12)
        selection_question.setFont(font)
        self.picker_button_0 = QPushButton('0')
        self.picker_button_0.setMinimumSize(100, 30)
        self.picker_button_0.clicked.connect(lambda num: self._picker_button_press(1))
        self.picker_button_1 = QPushButton('1')
        self.picker_button_1.clicked.connect(lambda num: self._picker_button_press(0))
        self.picker_button_1.setMinimumSize(100, 30)
        skip_button = QPushButton('Skip to Next Pair')
        skip_button.clicked.connect(self._skip_picker_selection)
        back_to_menu_button = QPushButton('Start Over')
        back_to_menu_button.clicked.connect(lambda x: self._return_to_home_screen(self.picker_layout))

        self.picker_layout.addWidget(bracket_button, 0, 0)
        self.picker_layout.addWidget(self.names_remaining, 1, 0)
        self.picker_layout.addWidget(QLabel(''), 2, 0)
        self.picker_layout.addWidget(QLabel(''), 3, 1)
        self.picker_layout.addWidget(QLabel(''), 4, 1)
        self.picker_layout.addWidget(selection_question, 5, 5)
        self.picker_layout.addWidget(self.picker_button_0, 6, 4)
        self.picker_layout.addWidget(self.picker_button_1, 6, 6)
        self.picker_layout.addWidget(skip_button, 7, 5)
        self.picker_layout.addWidget(QLabel(''), 8, 7)
        self.picker_layout.addWidget(QLabel(''), 9, 7)
        self.picker_layout.addWidget(QLabel(''), 10, 7)
        self.picker_layout.addWidget(QLabel(''), 11, 8)
        self.picker_layout.addWidget(QLabel(''), 12, 8)
        self.picker_layout.addWidget(back_to_menu_button, 13, 10)
        self.picker_layout.setSpacing(15)

        self.main_screen_layout.addLayout(self.picker_layout)

        self._reconfigure_info_button(picker_instructions, 'Instructions', 12)
        self._initiate_picking()

    def _show_bracket(self):
        remaining_names = '\n'.join(self.name_bank)
        self.display_info(f'The following names remain:\n{remaining_names}', 'Pseudo-Bracket', 12, True)

    def _skip_picker_selection(self):
        self.cur_name_stack.insert(0, self.cur_names)
        self._initiate_picking()

    def _initiate_picking(self):
            self._transition_end_screen_from_picker()

    def _transition_end_screen_from_picker(self):
        self._clear_layout(self.picker_layout)
        start_over_button = QPushButton('Start Over')
        start_over_button.clicked.connect(lambda x: self._return_to_home_screen(self.end_screen_layout))
        exit_button = QPushButton('Exit')
        exit_button.clicked.connect(self.close)
        final_message = QLabel(f'Your final name is: {self.name_bank[0]}!')
        font = final_message.font()
        font.setPointSize(20)
        final_message.setFont(font)
        self.end_screen_layout.addWidget(final_message, 0, 1)
        self.end_screen_layout.addWidget(start_over_button, 1, 0)
        self.end_screen_layout.addWidget(exit_button, 1, 2)
        self.end_screen_layout.setSpacing(20)
        self.main_screen_layout.addLayout(self.end_screen_layout)
        self._reconfigure_info_button(end_screen, 'Congratulations!', 12)

    def _picker_button_press(self, button: int):
        self.name_bank.remove(self.cur_names[button])
        self.names_remaining.setText(f'Names remaining: {len(self.name_bank)}')
        self._initiate_picking()

    def _populate_name_bank(self):
        num_choices = self.config_selections['num_choices']
        gender = self.config_selections['gender']

        if self.config_selections['source'] == 'Manual':
            # Existing logic for manual entry
            text_input = TextInputBox("Enter Names")
            text_input.text_entered.connect(self._get_manual_text)
            text_input.exec()
        else:
            # Fetch names from the Flask app
            try:
                response = requests.get(f'http://127.0.0.1:5000/get-baby-names', params={'gender': gender, 'num_names': num_choices})
                if response.ok:
                    self.name_bank = response.json()
                else:
                    raise Exception("Failed to fetch names from Flask app")
            except Exception as e:
                print(f"Error: {e}")

    def _get_manual_text(self, text):
        self.name_bank.extend(text.split('\n'))

    def _populate_name_stack(self):
        random.shuffle(self.name_bank)
        self.cur_name_stack = [(name_1, name_2) for name_1, name_2 in zip(self.name_bank[::2], self.name_bank[1::2])]

    def _clear_names(self):
        self.name_bank = []
        self.cur_name_stack = []
        self.cur_names = None

    def _build_home_screen_layout(self):
        start_message = QLabel('Push button to start!')
        start_button = QPushButton('Start')
        start_button.setFixedSize(QSize(100, 50))
        start_button.clicked.connect(self._transition_to_config)
        self.main_screen_layout.addWidget(start_message, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_screen_layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_screen_layout.setSpacing(10)
        self.main_screen_layout.setContentsMargins(0, 0, 0, 0)
        self._reconfigure_info_button(home_screen_info, 'Welcome', 16)

    def _populate_config_selections(self):
        self.config_selections['gender'] = self.gender_dropdown.currentText()
        self.config_selections['num_choices'] = int(self.num_choices_drowdown.currentText())
        self.config_selections['source'] = self.name_source_drowdown.currentText()

    def _clear_layout(self, layout):
        for i in range(layout.count()):
            if layout.itemAt(i).widget():
                # layout.itemAt(i).widget().disconnect()
                layout.itemAt(i).widget().deleteLater()
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            layout.removeItem(item)

    def display_info(self, message: str, title: str, font_size: int = 12, scrollable: bool = False):
        info_box = InformationDialog(message, title, font_size, scrollable)
        info_box.exec()


class InformationDialog(QDialog):
    def __init__(self, message: str, title: str, font_size: int = 12, scrollable: bool = False):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumWidth(400)  # Set the minimum width to 400 pixels
        self.setMinimumHeight(200)
        self.info = QLabel(message)
        self.font = self.info.font()
        self.font.setPointSize(font_size)
        self.info.setFont(self.font)
        if scrollable:
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(self.info)
        self.ok_button = QPushButton('Ok')
        self.ok_button.clicked.connect(self.accept)
        dialog_layout = QVBoxLayout()
        if scrollable:
            dialog_layout.addWidget(scroll_area)
        else:
            dialog_layout.addWidget(self.info)
        dialog_layout.addWidget(self.ok_button)
        self.setLayout(dialog_layout)


class TextInputBox(QDialog):
    text_entered = pyqtSignal(str)

    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        self.instructions = QLabel('Enter an even number of baby names, one per line.')
        self.text_edit = QPlainTextEdit()
        self.ok_button = QPushButton('Ok')
        self.ok_button.clicked.connect(self._get_text)
        self.layout.addWidget(self.instructions)
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.ok_button)
        self.setLayout(self.layout)

    def _get_text(self):
        split_text = self.text_edit.toPlainText().split('\n')
        if not split_text or not len(split_text) > 1 or not len(split_text) % 2 == 0:
            error = InformationDialog('Please enter an even number of names, at least two.', 'Error!', 12)
            error.exec()
            return
        self.text_entered.emit(self.text_edit.toPlainText())
        self.close()


if __name__ == '__main__':
    baby_name_picker = QApplication([])
    main_window = MainWindow()
    main_window.show()
    main_window.display_info(whats_new_screen, 'What\'s New?', 12)
    sys.exit(baby_name_picker.exec())