import sqlite3
import sys

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox


DB_NAME = "coffee.sqlite"


class AddEditForm(QtWidgets.QWidget):
    def __init__(self, parent=None, record=None):
        super().__init__(parent)
        uic.loadUi("addEditCoffeeForm.ui", self)

        self.record = record

        if record:
            self.lineName.setText(record[1])
            self.lineRoast.setText(record[2])
            self.lineGround.setText(record[3])
            self.lineDescription.setText(record[4])
            self.linePrice.setText(str(record[5]))
            self.lineVolume.setText(str(record[6]))

        self.btnSave.clicked.connect(self.save)

    def save(self):
        name = self.lineName.text().strip()
        roast = self.lineRoast.text().strip()
        ground = self.lineGround.text().strip()
        desc = self.lineDescription.text().strip()

        try:
            price = float(self.linePrice.text())
            volume = int(self.lineVolume.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Цена и объем должны быть числами.")
            return

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        if self.record:
            cur.execute("""
                UPDATE coffee
                SET name=?, roast=?, ground=?, description=?, price=?, volume=?
                WHERE id=?
            """, (name, roast, ground, desc, price, volume, self.record[0]))
        else:
            cur.execute("""
                INSERT INTO coffee (name, roast, ground, description, price, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, roast, ground, desc, price, volume))

        conn.commit()
        conn.close()

        self.close()
        self.parent().load_data()


class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.table = self.tableCoffee

        self.btnAdd.clicked.connect(self.add_record)
        self.btnEdit.clicked.connect(self.edit_record)

        self.load_data()

    def load_data(self):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        cur.execute("SELECT * FROM coffee")
        rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(7)

        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(value)))

        conn.close()

    def add_record(self):
        self.form = AddEditForm(self)
        self.form.show()

    def edit_record(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите строку для редактирования.")
            return

        record = []
        for col in range(7):
            record.append(self.table.item(row, col).text())

        record[0] = int(record[0])
        record[5] = float(record[5])
        record[6] = int(record[6])

        self.form = AddEditForm(self, record=record)
        self.form.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
