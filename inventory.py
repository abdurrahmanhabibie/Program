import sys
import numpy as np 
import csv

from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui

from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class Inventory(QMainWindow):
    def __init__(self):
        super(Inventory, self).__init__()
        loadUi("newinvent.ui", self)
        hheader = self.data_item.horizontalHeader()
        hheader.setSectionResizeMode(0,QHeaderView.ResizeToContents)
        hheader.setSectionResizeMode(1,QHeaderView.ResizeToContents)
        hheader.setSectionResizeMode(2,QHeaderView.Stretch)
        hheader.setSectionResizeMode(3,QHeaderView.ResizeToContents)
        hheader.setSectionResizeMode(4,QHeaderView.ResizeToContents)
        hheader.setSectionResizeMode(5,QHeaderView.ResizeToContents)

        now = QDateTime.currentDateTime()
        self.clock.setText(now.toString(Qt.DefaultLocaleLongDate))

        with open(r'Data\database-product.csv', mode= 'r') as csv_database:
            data_product = csv.DictReader(csv_database, delimiter=",")
            names = np.empty((0,1), str)
            for row in data_product:
            # auto complete options                                                 
                names = np.append(names,row["product_name"])
        completer = QCompleter(names)
        self.searchbar.setCompleter(completer)
        self.searchbar.setPlaceholderText("Search Item Here")

        self.scan()

    def scan(self):
        line_count = self.data_item.rowCount()
        with open(r'Data\database-product.csv', mode= 'r') as csv_database:
            data_product = csv.DictReader(csv_database, delimiter=",")
            for row in data_product:
                self.data_item.insertRow(line_count)
                self.data_item.setItem(line_count, 0, QtWidgets.QTableWidgetItem(row['product_code']))
                self.data_item.setItem(line_count, 1, QtWidgets.QTableWidgetItem(row['product_brand']))
                self.data_item.setItem(line_count, 2, QtWidgets.QTableWidgetItem(row['product_name']))
                if int(row['discount']) == 0:
                    self.data_item.setItem(line_count, 3, QtWidgets.QTableWidgetItem(str('-')))
                else:
                    self.data_item.setItem(line_count, 3, QtWidgets.QTableWidgetItem(row['product_name']))
                self.data_item.setItem(line_count, 4, QtWidgets.QTableWidgetItem(row['product_price'])) 
                self.data_item.setItem(line_count, 5, QtWidgets.QTableWidgetItem(row['product_stock']))
                if int(row['product_stock']) < 500:
                    self.setbgr(line_count)

                line_count += 1
    def setbgr(self,row):
        self.data_item.item(row,0).setBackground(QtGui.QColor(255,0,0))
        self.data_item.item(row,1).setBackground(QtGui.QColor(255,0,0))
        self.data_item.item(row,2).setBackground(QtGui.QColor(255,0,0))
        self.data_item.item(row,3).setBackground(QtGui.QColor(255,0,0))
        self.data_item.item(row,4).setBackground(QtGui.QColor(255,0,0))
        self.data_item.item(row,5).setBackground(QtGui.QColor(255,0,0))
        pass

if __name__== "__main__":
    app = QApplication(sys.argv)
    window = Inventory()
    window.setWindowTitle("Prototype UI Cashier")
    window.show()
    sys.exit(app.exec_())