import sqlite3
import sys

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class CreateAdd(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("add_create.ui", self)
        self.con = sqlite3.connect("coffee.db")
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.update)
        self.pushButton_3.clicked.connect(self.save_results)
        self.pushButton.clicked.connect(self.add_new)
        self.modified = {}
        self.titles = None

    def update(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("SELECT * FROM infromation WHERE id=?",
                             (item_id := self.spinBox.text(),)).fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с id = {item_id}")
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE infromation SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE id = ?"
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()
            self.modified.clear()

    def add_new(self):
        cur = self.con.cursor()
        cur.execute("SELECT COUNT(*) FROM infromation")
        count = cur.fetchall()
        id = 0
        for i in count:
            for j in i:
                id = int(j)
        first = self.plainTextEdit.toPlainText()
        second = self.plainTextEdit_2.toPlainText()
        third = self.plainTextEdit_4.toPlainText()
        fourth = self.plainTextEdit_3.toPlainText()
        fifth = self.plainTextEdit_5.toPlainText()
        sixth = self.plainTextEdit_6.toPlainText()
        params = (id + 1, first, second, third, fourth, fifth, sixth)
        cur.execute("""INSERT INTO infromation
           VALUES(?, ?, ?, ?, ?, ?, ?)""", params)
        self.con.commit()
        self.statusBar().showMessage(f'''Сохранена информация о кофе с индексом {id + 1}''')


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.db")
        self.add_form = CreateAdd()
        self.pushButton.clicked.connect(self.update_result)
        self.pushButton_2.clicked.connect(self.add_create)
        self.modified = {}
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("SELECT * FROM infromation WHERE id=?",
                             (item_id := self.spinBox.text(),)).fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с id = {item_id}")
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def add_create(self):
        self.add_form.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
