# Note: to make it executable app:
# python3 -m PyInstaller --onefile --windowed --add-data "icons:icons" --add-data "database.db:." main.py
import sys
from datetime import datetime
import sqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QToolBar, \
    QVBoxLayout, QLabel, QWidget, QBoxLayout,QStatusBar,\
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QDialog, QComboBox, QMessageBox
from PyQt6.QtGui import QAction, QIcon
from samba.kcc.graph import add_out_edge
from scipy.sparse import diags


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(700,500)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        search_action = QAction(QIcon("icons/icons/search.png"),"Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)


        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)  # if clicked on about, then call about method



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
        toolbar.addAction(search_action)

        # Crate status bar and add status bar elements
        self.statubar = QStatusBar()
        self.setStatusBar(self.statubar)
        #hello = QLabel("Hello There!")
        #statubar.addWidget(hello)
        #hello = QLabel("Hello World!")
        #statubar.addWidget(hello)
        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)  #by# click, the method edit should be called

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)  #by# click, the method edit should be called

        # Note: when we click on table data, it keeps showing both edit and delete button for each click! to stop it:
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statubar.removeWidget(child)


        self.statubar.addWidget(edit_button)
        self.statubar.addWidget(delete_button)

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

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This is a simple app which does student registration 
        interacting with database. 
        
        Feel free to use and develope it.
        Write me: 
        vakili.hu.it@gmail.com
        """
        self.setText(content)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data...")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Get student name from selected row
        index = main_window.table.currentRow()
        self.student_name = main_window.table.item(index, 1).text() # inded and sutdent name which ic in column 2
        # Get id from selected row
        self.student_id = main_window.table.item(index, 0).text()

        # Add student name widget
        self.student_name = QLineEdit(self.student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add combobox for courses
        self.coruse_name = main_window.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Math", "Physics", "AI", "Biology"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(self.coruse_name)
        layout.addWidget(self.course_name)

        # Add Mobile
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add a submit button
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)


    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("update students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(),
                       self.course_name.itemText(self.course_name.currentIndex()),
                       self.mobile.text(),
                       self.student_id))
        connection.commit() # to wrire operation happen
        cursor.close()
        connection.close()
        main_window.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data...")
        self.setFixedWidth(170)
        self.setFixedHeight(150)

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0 , 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1 )
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)

    def delete_student(self):
        #Get selected row index and student id
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (student_id, ))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data() # will access the data and somehow refresh it!

        self.close() # to close yes/no window! the current opening window
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The Record was deleted successfully!")
        confirmation_widget.exec()

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
        main_window.load_data()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Set window title and size
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        #Ccreate layout and input widget
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Create button
        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?",(name,))
        rows = list(result)
        print(rows)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()

#call load func to get data out of sqlserver
main_window.load_data()

sys.exit(app.exec())
