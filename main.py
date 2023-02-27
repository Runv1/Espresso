import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

import addeditui
import mainui


class LoadWidget(QDialog, addeditui.Ui_Dialog):
    def __init__(self, parent, con, id, name, stepen, molotiy, vkys, cost, volume, description):
        super().__init__(parent)
        self.con = con
        self.setupUi(self)
        self.lineEdit.setText(str(id))
        self.lineEdit_2.setText(str(name))
        self.lineEdit_3.setText(str(stepen))
        self.lineEdit_4.setText(str(molotiy))
        self.lineEdit_5.setText(str(vkys))
        self.lineEdit_6.setText(str(cost))
        self.lineEdit_7.setText(str(volume))
        self.lineEdit_8.setText(str(description))

        self.saveButton.clicked.connect(self.save)

    def save(self):
        try:
            if len(self.lineEdit.text()):
                id = self.lineEdit.text()
            else:
                id = None
            name = self.lineEdit_2.text()
            stepen = self.lineEdit_3.text()
            molotiy = self.lineEdit_4.text()
            vkys = self.lineEdit_5.text()
            cost = self.lineEdit_6.text()
            volume = self.lineEdit_7.text()
            description = self.lineEdit_8.text()
            cur = self.con.cursor()
            cur.execute(f"""
                    INSERT INTO coffee 
                    (
                       id,
                       name,
                       stepen,
                       molotiy,
                       vkys,
                       cost,
                       volume,
                       description
                   )
                   VALUES (?,?,?,?,?,?,?,?)
                    ON CONFLICT(id) DO
                    UPDATE SET name = ?,
                       stepen = ?,
                       molotiy = ?,
                       vkys = ?,
                       cost = ?,
                       volume = ?,
                       description = ?
                    """,
                        (
                            id, name, stepen, molotiy, vkys, cost, volume, description, name, stepen,
                            molotiy,
                            vkys, cost, volume, description)
                        )
            self.con.commit()
            self.accept()
        except Exception as e:
            print(e)
            self.error_message.setText('Неверно заполнена форма')


class MyWidget(QMainWindow, mainui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.tableWidget.clicked.connect(self.select_row)
        self.pushButton.clicked.connect(self.add_row)
        self.load_table()

    def select_row(self, item):
        values = []
        for i in range(self.tableWidget.columnCount()):
            values.append(self.tableWidget.item(item.row(), i).text())
        dialog = LoadWidget(self, self.con, *values)
        if dialog.exec_() == QDialog.Accepted:
            self.load_table()

    def add_row(self):
        values = [""] * 8
        dialog = LoadWidget(self, self.con, *values)
        if dialog.exec_() == QDialog.Accepted:
            pass
        self.load_table()

    def get_data(self):
        q = """SELECT * FROM coffee"""
        return self.con.cursor().execute(q).fetchall()

    def load_table(self):
        try:
            self.tableWidget.setRowCount(0);
            result = self.get_data()
            self.tableWidget.setColumnCount(8)
            self.tableWidget.setHorizontalHeaderLabels(
                ['id', 'name', 'stepen', 'molotiy', 'vkys', 'cost', 'volume', 'description'])
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
