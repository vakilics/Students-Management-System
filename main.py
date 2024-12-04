import sys
from datetime import datetime
import sqlite3

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt6.QtWidgets import QApplication,QTableWidget,QTableWidgetItem, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow
from PyQt6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False) # hide duplicate index numbering in Table
        # To display table on GUI!
        self.setCentralWidget(self.table)

    # fill the table with DB data!
    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        #result = connection.execute("SELECT * FROM students WHERE name='Hamid Vakili'")
        #print(list(result))
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):                                  # get each row's number and its data:  0, Hamid, Math,015700000
            self.table.insertRow(row_number)                                            # insert empty row in particular index: 0,...
            for column_number, data in enumerate(row_data):                             # inset the taken data into each row!
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data))) # now we have row and column, so insert actual data!
        connection.close()


app = QApplication(sys.argv)
age_calculator = MainWindow()
age_calculator.show()

#call load func to get data out of sqlserver
age_calculator.load_data()

sys.exit(app.exec())