from socket import create_server

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QLineEdit, \
    QGridLayout, QPushButton, QComboBox, QMainWindow, QTableWidget, QTableWidgetItem,\
    QDialog
from PyQt6.QtGui import QAction
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        # self.setFixedHeight(500)
        # self.setFixedWidth(500)

        # Menu bar refers to the menu of options that appears at the top of the window
        file_menubar_item = self.menuBar().addMenu("&File")
        help_menubar_item = self.menuBar().addMenu("&Help")
        edit_menubar_item = self.menuBar().addMenu("&Edit")


        # subitems within the dropdown menus on the top of the window are known as "actions"

        add_student_action = QAction("Add Student", self) # creating "actions"
        add_student_action.triggered.connect(self.insert) #push buttons are "clicked", and menu actions are "triggered"
        file_menubar_item.addAction(add_student_action) # adding actions to their respective menubar options

        about_action = QAction("About", self)
        help_menubar_item.addAction(about_action)

        search_action = QAction("Search", self)
        search_action.triggered.connect(self.search)
        edit_menubar_item.addAction(search_action)



        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID","Name","Course","Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)


    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute('SELECT * FROM students')
        self.table.setRowCount(0)
        for row_index, row_data in enumerate(result):
            self.table.insertRow(row_index)
            for column_index, column_data in enumerate(row_data):
                self.table.setItem(row_index, column_index,
                                   QTableWidgetItem(str(column_data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        insert_student_layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        insert_student_layout.addWidget(self.student_name)


        self.courses = QComboBox()
        courses_list = ["Biology", "Maths","Astronomy", "Physics"]
        self.courses.addItems(courses_list)
        insert_student_layout.addWidget(self.courses)


        self.student_number = QLineEdit()
        self.student_number.setPlaceholderText("Number")
        insert_student_layout.addWidget(self.student_number)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.add_student)
        insert_student_layout.addWidget(self.submit_button)

        self.setLayout(insert_student_layout)


    def add_student(self):
        name = self.student_name.text()
        course = self.courses.itemText(self.courses.currentIndex())
        mobile = self.student_number.text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name,course,mobile) VALUES (?, ?, ?)",
                       (name,course,mobile))
        connection.commit()
        cursor.close()
        connection.close()
        student_management.load_data()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Search")
        self.setFixedHeight(500)
        self.setFixedWidth(500)

        search_box_layout = QVBoxLayout()

        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Name")

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_student)

        search_box_layout.addWidget(self.search_name)
        search_box_layout.addWidget(search_button)

        self.setLayout(search_box_layout)

    def search_student(self):
        name = self.search_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM events WHERE name=?", (name))
        present_rows = cursor.fetchall()
        print(present_rows)










app = QApplication(sys.argv)
student_management = MainWindow()
student_management.load_data()
student_management.show()
sys.exit(app.exec())