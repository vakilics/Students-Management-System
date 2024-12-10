import sys
from datetime import datetime
import sqlite3

from PyQt5.QtWidgets import QDialog
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QToolBar, \
    QVBoxLayout, QLabel, QWidget, QBoxLayout, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QDialog, QComboBox
from PyQt6.QtGui import QAction, QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction(QIcon("icons/icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)  # hide duplicate index numbering in Table
        # To display table on GUI!
        self.setCentralWidget(self.table)

        # Add toolbar and add toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)

    # fill the table with DB data!
    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        #result = connection.execute("SELECT * FROM students WHERE name='Hamid Vakili'")
        #print(list(result))
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):  # get each row's number and its data:  0, Hamid, Math,015700000
            self.table.insertRow(row_number)  # insert empty row in particular index: 0,...
            for column_number, data in enumerate(row_data):  # inset the taken data into each row!
                self.table.setItem(row_number, column_number,
                                   QTableWidgetItem(str(data)))  # now we have row and column, so insert actual data!
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


# to create dialog window. eg: click add student, then opens a dialog window to fill
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data...")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add combobox for courses
        self.course_name =QComboBox()
        courses = ["Math", "Physics", "AI"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add Mobile
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add a submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        # to apply the changes
        connection.commit()
        cursor.close()
        connection.close()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()

#call load func to get data out of sqlserver
main_window.load_data()

sys.exit(app.exec())
