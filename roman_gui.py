from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QHBoxLayout, QApplication, QComboBox,
                             QLineEdit, QWidget, QPushButton, QMainWindow,
                             QAction, QTextEdit)
from PyQt5.QtCore import Qt
import sys
from roman import choose_method
import os

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # creating roman widget and setting it as central
        self.roman_widget = Window(parent=self)
        self.setCentralWidget(self.roman_widget)

        # filling up a menu bar
        bar = self.menuBar()

        # File menu
        file_menu = bar.addMenu('File')
        # adding actions to file menu
        open_action = QAction('Open', self)
        close_action = QAction('Close', self)
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)

        # Edit menu
        edit_menu = bar.addMenu('Edit')
        # adding actions to edit menu
        undo_action = QAction('Undo', self)
        redo_action = QAction('Redo', self)
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        # use `connect` method to bind signals to desired behavior
        close_action.triggered.connect(self.close)
        self.setWindowTitle("Roman Numerals")

class Window(QWidget):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setup_ui()
        self.printed = []

    def setup_ui(self):
        # Setup all items to appear on screen
        self.label_1 = QLabel('Argument 1')
        self.label_2 = QLabel('Argument 2')
        self.arg_box_1 = QLineEdit()
        self.arg_box_2 = QLineEdit()
        self.type_op = QComboBox()
        self.calculate = QPushButton('Calculate')
        self.result_label = QLabel('Result:')
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)

        # Add tooltips
        self.arg_box_1.setToolTip('Integers or strings only')
        self.arg_box_2.setToolTip('Integers or strings only')

        # Populate drop down box
        self.type_op.addItems(['add', 'subtract', 'multiply', 'divide', 'power', 'modulo', 'convert'])

        # Setup call for calculate button
        self.calculate.clicked.connect(self.do_operation)

        # Initialise Horizontal box for labels
        v_box_arg1 = QVBoxLayout()
        v_box_arg1.addWidget(self.label_1)
        v_box_arg1.addWidget(self.arg_box_1)

        v_box_arg2 = QVBoxLayout()
        v_box_arg2.addWidget(self.label_2)
        v_box_arg2.addWidget(self.arg_box_2)

        h_box_args = QHBoxLayout()
        h_box_args.addLayout(v_box_arg1)
        h_box_args.addLayout(v_box_arg2)
        h_box_args.addStretch()

        # Initialise Horizontal box with drop down box and calculate button
        h_box_controls = QHBoxLayout()
        h_box_controls.addWidget(self.type_op)
        h_box_controls.addWidget(self.calculate)
        h_box_controls.addStretch()

        h_box_results = QHBoxLayout()
        h_box_results.addWidget(self.result_label)
        h_box_results.addWidget(self.result)

        # Initialise Vertical box containing the Horizontal Boxes and results box
        v_box = QVBoxLayout()
        v_box.addLayout(h_box_args)
        v_box.addLayout(h_box_controls)
        #v_box.addStretch()
        v_box.addLayout(h_box_results)

        self.setMinimumHeight(150)
        self.setMinimumWidth(500)
        self.setLayout(v_box)

    def do_operation(self):
        arg1 = self.arg_box_1.text()
        arg2 = self.arg_box_2.text()
        operation = str(self.type_op.currentText())
        self.printed.append(f"Result of {operation} with arg1: {arg1} and arg2: {arg2} = "
                            f"{str(choose_method(arg1, arg2, operation))}")
        output = "\n".join(self.printed)
        self.result.setText(output)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
