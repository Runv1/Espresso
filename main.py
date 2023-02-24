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
        self.load_table()

    def get_data(self):
        q = """SELECT * FROM coffee"""
        return self.cur.execute(q).fetchall()

    def load_table(self):
        try:
            result = self.get_data()
            self.tableWidget.setColumnCount(7)
            self.tableWidget.setHorizontalHeaderLabels(['id', 'name', 'stepen', 'molotiy', 'vkys', 'cost', 'volume'])
            self.tableWidget.setRowCount(len(result))
            for i, row in enumerate(result):
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
