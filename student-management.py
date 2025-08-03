from socket import create_server

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QLineEdit, \
    QGridLayout, QPushButton, QComboBox, QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3
import mysql.connector

# from PyQt6.QtWidgets.QMainWindow import contextMenuEvent


# from PyQt6.QtWidgets.QMainWindow import childEvent


# DB_FILE = "database.db"
# class DatabaseConnection:
#     def __init__(self, db_file = DB_FILE):
#         self.db_file = db_file
#
#     def connection(self):
#         self.connection = sqlite3.connect(self.db_file)
#         return self.connection

class DatabaseConnection:
    def __init__(self, host = "localhost", user="root", password = "pythoncourse",db = "school"):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def connection(self):
        connection = mysql.connector.connect(host = self.host, user=self.user, password = self.password ,db = self.db)
        return connection

# we now can use it in this format: DatabaseConnection().connect()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(600,600)
        # self.setFixedHeight(500)
        # self.setFixedWidth(500)

        # Menu bar refers to the menu of options that appears at the top of the window
        file_menubar_item = self.menuBar().addMenu("&File")
        help_menubar_item = self.menuBar().addMenu("&Help")
        edit_menubar_item = self.menuBar().addMenu("&Edit")


        # subitems within the dropdown menus on the top of the window are known as "actions"

        add_student_action = QAction(QIcon("icons/add.png"),"Add Student", self) # creating "actions"
        add_student_action.triggered.connect(self.insert) #push buttons are "clicked", and menu actions are "triggered"
        file_menubar_item.addAction(add_student_action) # adding actions to their respective menubar options

        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_menubar_item.addAction(about_action)

        search_action = QAction(QIcon("icons/search.png"),"Search", self)
        search_action.triggered.connect(self.search)
        edit_menubar_item.addAction(search_action)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        # uses the already existing "action" - that also where it gets the text to display from
        toolbar.addAction(search_action)


        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID","Name","Course","Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.table.cellClicked.connect(self.cell_clicked)

    def load_data(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM students')
        result = cursor.fetchall()
        self.table.setRowCount(0) # reset number of rows shown to zero
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

    def cell_clicked(self):
        children = self.findChildren(QPushButton) # find all QPushButton objects on main window.
        if children: # Iterates through the list if it exists
            print(list(children))
            for child in children:
                self.status_bar.removeWidget(child) # removes the QPushButton objects present on the status bar
                # If the QPushButton isn't present on status bar but rather somewhere else it'll probably be ignored
                # (That's my potentially flawed understanding)


        edit_button = QPushButton("Edit Record")
        self.status_bar.addWidget(edit_button)
        edit_button.clicked.connect(self.edit_record)

        delete_button = QPushButton("Delete Record")
        self.status_bar.addWidget(delete_button)
        delete_button.clicked.connect(self.delete_record)

    def edit_record(self):
        dialog = EditDialog()
        dialog.exec()

    def delete_record(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
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

        connection = DatabaseConnection().connect()
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
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE name=?", (name,))
        result = cursor.fetchall()
        rows = list(result)
        print(rows)
        items = student_management.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            student_management.table.item(item.row(),1).setSelected(True)
        cursor.close()
        connection.close()

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Student Data")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        edit_student_layout = QVBoxLayout()

        index = student_management.table.currentRow() # returns an integer

        self.id_pre_edit = student_management.table.item(index, 0).text()
        name_pre_edit = student_management.table.item(index, 1).text()
        course_pre_edit = student_management.table.item(index,2).text()
        number_pre_edit = student_management.table.item(index,3).text()


        self.student_name = QLineEdit(name_pre_edit)
        self.student_name.setPlaceholderText("Name")
        edit_student_layout.addWidget(self.student_name)


        self.courses = QComboBox()
        courses_list = ["Biology", "Maths","Astronomy", "Physics"]
        self.courses.addItems(courses_list)
        self.courses.setCurrentText(course_pre_edit)
        edit_student_layout.addWidget(self.courses)


        self.student_number = QLineEdit(number_pre_edit)
        self.student_number.setPlaceholderText("Number")
        edit_student_layout.addWidget(self.student_number)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.edit_student)
        edit_student_layout.addWidget(self.submit_button)

        self.setLayout(edit_student_layout)

    def edit_student(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        edited_course = self.courses.itemText(self.courses.currentIndex())
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id=?",
                       (self.student_name.text(),edited_course,self.student_number.text(), self.id_pre_edit))
        connection.commit()
        cursor.close()
        connection.close()
        student_management.load_data()

class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Record")
        self.setFixedHeight(100)
        self.setFixedWidth(400)

        delete_student_layout = QGridLayout()

        conformation_text = QLabel("Are you sure you would like to delete this student record?")
        delete_student_layout.addWidget(conformation_text,0,0,1,2)

        conformation_button_yes = QPushButton("Yes")
        conformation_button_no = QPushButton("No")
        delete_student_layout.addWidget(conformation_button_yes,1,0)
        delete_student_layout.addWidget(conformation_button_no,1,1)

        conformation_button_yes.clicked.connect(self.delete_record)

        self.setLayout(delete_student_layout)

    def delete_record(self):
        index = student_management.table.currentRow()
        self.id = student_management.table.item(index, 0).text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM students WHERE id = ?",(self.id,))
        connection.commit()
        cursor.close()
        connection.close()
        student_management.load_data()
        delete_message_box = QMessageBox()
        delete_message_box.setWindowTitle("Delete operation successful")
        delete_message_box.setText("Deleted student record successfully.")
        self.close()
        delete_message_box.exec()

# class AboutDialog(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("About")
#         self.setFixedHeight(300)
#         self.setFixedWidth(300)
#
#         about_dialog_layout = QVBoxLayout()
#
#         about_text = QLabel("Insert helpful text here and call it a day.")
#         about_dialog_layout.addWidget(about_text)
#
#         self.setLayout(about_dialog_layout)

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setText("Insert helpful text here and call it a day.")
        self.exec()








app = QApplication(sys.argv)
student_management = MainWindow()
student_management.load_data()
student_management.show()
sys.exit(app.exec())