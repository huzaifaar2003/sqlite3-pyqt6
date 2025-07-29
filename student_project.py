from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QLineEdit, \
    QGridLayout, QPushButton, QComboBox
import sys

class AverageSpeed(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Average Speed Calculator")

        grid = QGridLayout()

        distance_label = QLabel("Distance: ")
        self.distance_line_edit = QLineEdit()

        time_label = QLabel("Time (hours): ")
        self.time_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate Average Speed")
        calculate_button.clicked.connect(self.calculate_speed)

        self.output_speed = QLabel("")

        self.units_combo = QComboBox()
        self.units_combo.addItems(['Miles (mi)', 'Kilometers (km)'])





        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_edit, 0, 1)
        grid.addWidget(self.units_combo, 0, 2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)

        grid.addWidget(calculate_button, 2, 0)
        grid.addWidget(self.output_speed, 3, 0)
        self.setLayout(grid)


    def calculate_speed(self):
        distance = float(self.distance_line_edit.text())
        time = float(self.time_line_edit.text())
        self.speed = distance/time

        if self.units_combo.currentText() == 'Miles (mi)':
            self.units = "mph"

        if self.units_combo.currentText() == 'Kilometers (km)':
            self.units = "kmh"

        self.output_speed.setText(f"Speed is {self.speed} {self.units}")
        # return self.speed








app = QApplication(sys.argv)
speed_calculator = AverageSpeed()
speed_calculator.show()
# speed_calculator.calculate_speed()
sys.exit(app.exec())