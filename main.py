import sqlite3
import sys

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem


DB_NAME = "coffee.sqlite"


class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("main.ui", self)

        self.table = self.findChild(QtWidgets.QTableWidget, "tableCoffee")

        self.load_data()

    def load_data(self):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name, roast, ground, description, price, volume
            FROM coffee
        """)
        rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(7)

        for row_index, row in enumerate(rows):
            for col_index, value in enumerate(row):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

        conn.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
