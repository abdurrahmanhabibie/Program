import sys
import numpy as np 
import csv

from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui

from PyQt5.QtCore import QDateTime, QEasingCurve, QPropertyAnimation, Qt
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class NewInvoice(QMainWindow):
    def __init__(self):
        super(NewInvoice, self).__init__()
        loadUi("newinvoice.ui", self)
        hheader = self.data_item.horizontalHeader()
        hheader.setSectionResizeMode(QHeaderView.Stretch)

        with open(r'Data/invoice.csv', mode= 'r') as csv_database:
            data_product = csv.DictReader(csv_database, delimiter=",")
            names = np.empty((0,1), str)
            for row in data_product:
            # auto complete options                                                 
                names = np.append(names,row["invoice"])
        completer = QCompleter(names)
        self.searchbar.setCompleter(completer)
        self.searchbar.setPlaceholderText("Search Item Here")

        self.scan()
        self.menu.clicked.connect(self.sidemenu)

    def scan(self):
        line_count = self.data_item.rowCount()
        with open(r'Data/invoice.csv', mode= 'r') as csv_database:
            data_product = csv.DictReader(csv_database, delimiter=",")
            for row in data_product:
                self.data_item.insertRow(line_count)
                self.data_item.setItem(line_count, 0, QtWidgets.QTableWidgetItem(row['invoice']))
                self.data_item.setItem(line_count, 1, QtWidgets.QTableWidgetItem(row['date']))
                self.data_item.setItem(line_count, 2, QtWidgets.QTableWidgetItem(str('Rp. ')+row['amount']))
                if int(row['amount']) < 500:
                    self.setbgr(line_count)

                line_count += 1

    def sidemenu(self):
        width = self.sidebar_ext.width()
        if width == 0:
            newWidth = 200
        else: 
            newWidth = 0
        self.animation = QPropertyAnimation(self.sidebar_ext, b"maximumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()

    def setbgr(self,row):
        self.data_item.item(row,0).setBackground(QtGui.QColor(255,0,0))
        self.data_item.item(row,1).setBackground(QtGui.QColor(255,0,0))
        self.data_item.item(row,2).setBackground(QtGui.QColor(255,0,0))
        self.data_item.item(row,3).setBackground(QtGui.QColor(255,0,0))
        self.data_item.item(row,4).setBackground(QtGui.QColor(255,0,0))
        pass

if __name__== "__main__":
    app = QApplication(sys.argv)
    window = NewInvoice()
    window.setWindowTitle("Prototype UI Cashier")
    window.show()
    sys.exit(app.exec_())
