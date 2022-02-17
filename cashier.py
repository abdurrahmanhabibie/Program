# Adding Necessary Library
import sys
import numpy as np 
import csv

from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui

from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class Cashier(QMainWindow):
    def __init__(self):
        super(Cashier, self).__init__()
        loadUi("main.ui", self)
        hheader = self.data_item.horizontalHeader()
        hheader.setSectionResizeMode(QHeaderView.Stretch)

        now = QDateTime.currentDateTime()
        self.clock.setText("  "+now.toString(Qt.DefaultLocaleLongDate))

        with open(r'file\database-product.csv', mode= 'r') as csv_database:
            data_product = csv.DictReader(csv_database, delimiter=",")
            names = np.empty((0,1), str)
            for row in data_product:
            # auto complete options                                                 
                names = np.append(names,row["product_name"])
        completer = QCompleter(names)
        self.searchbar.setCompleter(completer)
        self.searchbar.setPlaceholderText("Search Item Here")
        self.NewData()
        
        self.btn_add.clicked.connect(self.insert)
        self.btn_scan.clicked.connect(self.scan)
        self.btn_pay.clicked.connect(self.pay)
        

    def insert(self):
        line_count = self.data_item.rowCount()
        text = self.searchbar.text()
        if len(self.subtotal_num.toPlainText()) > 0:   
            subtotal = int(self.subtotal_num.toPlainText())
        else:
            subtotal = 0
        discount = 0
        if text != "":
            with open(r'file\database-product.csv', mode= 'r') as csv_database:
                data_product = csv.DictReader(csv_database, delimiter=",")
                for row in data_product:
                    if text == row["product_name"]:
                        temp = False
                        if self.data_item.rowCount()==0:
                                print("cart is empty")
                                self.data_item.insertRow(line_count)
                                self.data_item.setItem(line_count, 1, QtWidgets.QTableWidgetItem(row['product_name']))
                                self.data_item.setItem(line_count, 2, QtWidgets.QTableWidgetItem("1"))
                                self.data_item.setItem(line_count, 0, QtWidgets.QTableWidgetItem(row['product_code']))
                                self.data_item.setItem(line_count, 3, QtWidgets.QTableWidgetItem(row['product_price'])) 
                                subtotal += int(row['product_price'])
                        for data in range(line_count):
                            if text == self.data_item.item(data,1).text():
                                qty = int(self.data_item.item(data,2).text()) + 1
                                self.data_item.setItem(data, 2, QtWidgets.QTableWidgetItem(str(qty)))
                                subtotal += int(row['product_price'])
                                temp = True
                            elif data == line_count-1 and temp == False:
                                self.data_item.insertRow(line_count)
                                self.data_item.setItem(line_count, 1, QtWidgets.QTableWidgetItem(row['product_name']))
                                self.data_item.setItem(line_count, 2, QtWidgets.QTableWidgetItem("1"))
                                self.data_item.setItem(line_count, 0, QtWidgets.QTableWidgetItem(row['product_code']))
                                self.data_item.setItem(line_count, 3, QtWidgets.QTableWidgetItem(row['product_price']))
                                subtotal += int(row['product_price']) 
        else:
            self.searchbar.setPlaceholderText("isi dulu")
        total = subtotal - discount
        self.display_bill(subtotal,discount,total)   

    
    # def scan(self):
    #     while self.data_item.rowCount() == 0:
    #         self.load_data()

    
    def scan(self):
        with open('data-cart.csv',mode= 'r') as csv_file:
            data_cart = csv.DictReader(csv_file, delimiter=",")
            line_count = self.data_item.rowCount()
            if len(self.subtotal_num.toPlainText()) > 0:   
                subtotal = int(self.subtotal_num.toPlainText())
            else:
                subtotal = 0
            discount = 0
            temp = True
            for data in data_cart:
                with open(r'file\database-product.csv', mode= 'r') as csv_database:
                    data_product = csv.DictReader(csv_database, delimiter=",")
                    # if temp ==  False:
                    #     for line in range(line_count):
                    #         if data["product_name"] == self.data_item.item(line,1).text() and temp == False:
                    #             print(self.data_item.item(line,1).text())
                    #             print('data udah ada')
                    #             qty = int(self.data_item.item(line,2).text()) + int(data['Qty'])
                    #             self.data_item.setItem(line, 2, QtWidgets.QTableWidgetItem(str(qty)))
                    #             subtotal += int(row['product_price'])*int(data['Qty'])
                    #     temp = True
                    for row in data_product:
                        if data["product_name"]==row["product_name"]:
                            for line in range(line_count):
                                if row["product_name"] == self.data_item.item(line,1).text():
                                    qty = int(self.data_item.item(line,2).text()) + int(data['Qty'])
                                    self.data_item.setItem(line, 2, QtWidgets.QTableWidgetItem(str(qty)))
                                    subtotal += int(row['product_price'])*int(data['Qty'])
                                    temp = False
                            if temp:    
                                self.data_item.insertRow(line_count)
                                self.data_item.setItem(line_count, 1, QtWidgets.QTableWidgetItem(data['product_name']))
                                self.data_item.setItem(line_count, 2, QtWidgets.QTableWidgetItem(data['Qty']))
                                self.data_item.setItem(line_count, 0, QtWidgets.QTableWidgetItem(row['product_code']))
                                self.data_item.setItem(line_count, 3, QtWidgets.QTableWidgetItem(row['product_price']))    
                                subtotal += int(data['Qty'])*int(row['product_price'])
                                line_count += 1
                        
        # print(subtotal)
        total = subtotal - discount
        self.display_bill(subtotal,discount,total)
    
    def pay(self):
        self.NewData()
        if self.searchbar.text() != "Search Item Here":
            self.searchbar.setText("")

    def NewData(self):
        while self.data_item.rowCount() > 0:
            self.data_item.removeRow(self.data_item.rowCount()-1)
        subtotal = 0
        discount = 0
        total= 0
        self.display_bill(subtotal,discount,total)

    def display_bill(self,x,y,z):
        self.erase_previous_bill()
        self.display_subtotal(x)
        self.display_discount(y)
        self.display_total(z)
    
    def erase_previous_bill(self):
        cursor = self.subtotal_num.textCursor()
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        cursor.removeSelectedText()
        cursor = self.discount_num.textCursor()
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        cursor.removeSelectedText()
        cursor = self.total_num.textCursor()
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        cursor.removeSelectedText()

    def display_subtotal(self,text):
        self.subtotal_num.append(str(text))
        self.subtotal_num.setAlignment(QtCore.Qt.AlignRight)
    def display_discount(self,text):
        self.discount_num.append(str(text))
        self.discount_num.setAlignment(QtCore.Qt.AlignRight)
    def display_total(self,text):
        self.total_num.append(str(text))
        self.total_num.setAlignment(QtCore.Qt.AlignRight)

if __name__== "__main__":
    app = QApplication(sys.argv)
    window = Cashier()
    window.setWindowTitle("Prototype UI Cashier")
    window.show()
    sys.exit(app.exec_())
