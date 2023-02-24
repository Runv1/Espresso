import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.con.set_trace_callback(print)
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.start_search)
        self.pushButton.clicked.connect(self.loadTable)

    def start_search(self):
        try:
            q = """SELECT * FROM coffee"""
            self.result = self.cur.execute(q).fetchall()
            print(self.result)
        except Exception as e:
            print(e)

    def loadTable(self):
        try:
            self.tableWidget.setColumnCount(7)
            self.tableWidget.setHorizontalHeaderLabels(['id', 'name', 'stepen', 'molotiy', 'vkys', 'cost', 'volume'])
            self.tableWidget.setRowCount(len(self.result) - 1)
            for i, row in enumerate(self.result):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(elem))
            self.tableWidget.resizeColumnsToContents()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())



