from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QLineEdit, \
    QGridLayout, QPushButton, QComboBox

import sys
from datetime import datetime

class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Age Calculator")
        # calling the __init__() method of super class before overwriting the __init__
        # method inthe child class
        grid = QGridLayout()

        name_label = QLabel("Name: ")
        self.name_line_edit = QLineEdit()
        dob_label = QLabel("Date of birth MM/DD/YYYY: ")
        self.dob_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate Age")
        calculate_button.clicked.connect(self.calculate_age)
        self.output_age = QLabel("") #Empty string currently. Will be set later

        grid.addWidget(name_label, 0, 0) #0,0 (row, column) is the position - top left
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(dob_label, 1, 0)
        grid.addWidget(self.dob_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 0, 1, 2)
        # 2,0,1,2: "2,0" is position:(row,column).
        # "1,2" is space occupied (rows, columns0
        grid.addWidget(self.output_age)
        self.setLayout(grid)

    def calculate_age(self):
        current_year = datetime.now().year
        date_of_birth = self.dob_line_edit.text()
        year_of_birth = datetime.strptime(date_of_birth,"%m/%d/%Y").date().year
        age = current_year - year_of_birth
        self.output_age.setText(f"{self.name_line_edit.text()} is {age} years old")


app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
# age_calculator.calculate_age()
sys.exit(app.exec())




