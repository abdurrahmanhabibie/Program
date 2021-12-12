# Adding Necessary Library
import sys
import numpy as np 
import csv

from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui

from PyQt5.QtCore import QDateTime, QEasingCurve, QPropertyAnimation, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.uic import loadUi

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.user.setPlaceholderText("  Enter Username Here")
        self.password.setPlaceholderText("  Enter Password Here")
        self.password.setEchoMode(QLineEdit.Password)

        with open(r'Data\user-temp.csv', mode= 'r') as csv_database:
            data_product = csv.DictReader(csv_database, delimiter=",")
            user = np.empty((0,1), str)
            password = np.empty((0,1), str)
            for row in data_product:
            # auto complete options                                                 
                user = np.append(user,row["user"])
                password = np.append(password,row["password"])
        completer = QCompleter(user)
        self.user.setCompleter(completer)

        self.login.clicked.connect(self.loginfunction)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.loginfunction()
    
    def loginfunction(self):
        with open(r'Data\data-user.csv', mode= 'r') as csv_database:
            data_user = csv.DictReader(csv_database, delimiter=",")
            for username in data_user:
                if self.user.text() == username['Name']:
                    if self.password.text() == username['Password']:
                        with open(r'Data/user-temp.csv', mode='w', newline='') as csv_file:
                            fieldnames = ['user', 'password']
                            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerow({'user': self.user.text(), 'password': self.password.text()})
                        print('login complete')
                        self.error.setText("")
                        self.user.clear()
                        self.password.clear()
                        self.gotocashier()
                    else:
                        self.error.setText("Invalid username or password")
    
    def gotocashier(self):
        gotoCashier = Cashier()
        widget.addWidget(gotoCashier)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Cashier(QMainWindow):
    def __init__(self):
        super(Cashier, self).__init__()
        loadUi("newcash.ui", self)
        hheader = self.data_item.horizontalHeader()
        hheader.setSectionResizeMode(QHeaderView.Stretch)

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
        self.data_item.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.btn_add.clicked.connect(self.insert)
        self.btn_scan.clicked.connect(self.scan)
        self.btn_pay.clicked.connect(self.pay)
        self.menu.clicked.connect(self.sidemenu)
        self.btn_pending.clicked.connect(self.pending)
        self.temp.clicked.connect(self.cart_temp)
        self.btn_sub.clicked.connect(self.delete)
        self.home.clicked.connect(self.NewData)
        self.logout.clicked.connect(self.gotologin)
        self.invoice.clicked.connect(self.gotoinvoice)
        self.inventory.clicked.connect(self.gotoinventory)

    def sidemenu(self):
        width = self.sidebar_ext.width()
        if width == 55:
            newWidth = 230
        else: 
            newWidth = 55
        self.animation = QPropertyAnimation(self.sidebar_ext, b"maximumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()


    def insert(self):
        line_count = self.data_item.rowCount()
        rows = set()
        for index in self.data_item.selectedIndexes():
            rows.add(index.row())
        text = self.searchbar.text()
        if len(self.subtotal_num.toPlainText()) > 0:   
            subtotal = int(self.subtotal_num.toPlainText())
            discount = int(self.discount_num.toPlainText())
        else:
            subtotal = 0
            discount = 0
        if text != "":
            with open(r'Data\database-product.csv', mode= 'r') as csv_database:
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
                                self.data_item.setItem(line_count, 3, QtWidgets.QTableWidgetItem(row['discount']))
                                self.data_item.setItem(line_count, 4, QtWidgets.QTableWidgetItem(row['product_price'])) 
                                subtotal += int(row['product_price'])
                                discount += int(row['discount'])
                        for data in range(line_count):
                            if text == self.data_item.item(data,1).text():
                                qty = int(self.data_item.item(data,2).text()) + 1
                                self.data_item.setItem(data, 2, QtWidgets.QTableWidgetItem(str(qty)))
                                subtotal += int(row['product_price'])
                                discount += int(row['discount'])
                                temp = True
                            elif data == line_count-1 and temp == False:
                                self.data_item.insertRow(line_count)
                                self.data_item.setItem(line_count, 1, QtWidgets.QTableWidgetItem(row['product_name']))
                                self.data_item.setItem(line_count, 2, QtWidgets.QTableWidgetItem("1"))
                                self.data_item.setItem(line_count, 0, QtWidgets.QTableWidgetItem(row['product_code']))
                                self.data_item.setItem(line_count, 3, QtWidgets.QTableWidgetItem(row['discount']))
                                self.data_item.setItem(line_count, 4, QtWidgets.QTableWidgetItem(row['product_price']))
                                subtotal += int(row['product_price'])
                                discount += int(row['discount']) 
            #self.searchbar.clear()
        elif len(rows) != 0:
            for row in sorted(rows, reverse=True):
                qty = int(self.data_item.item(row,2).text()) + 1
                self.data_item.setItem(row, 2, QtWidgets.QTableWidgetItem(str(qty)))
                subtotal += int(self.data_item.item(row,4).text())
                discount += int(self.data_item.item(row,3).text())
        else:
            self.searchbar.setPlaceholderText("isi dulu")
        total = subtotal - discount
        self.display_bill(subtotal,discount,total)   

    def delete(self):
        rows = set()
        for index in self.data_item.selectedIndexes():
            rows.add(index.row())
        if len(self.subtotal_num.toPlainText()) > 0:   
            subtotal = int(self.subtotal_num.toPlainText())
            discount = int(self.discount_num.toPlainText())
        else:
            subtotal = 0
            discount = 0
        if len(rows) != 0:
            for row in sorted(rows, reverse=True):
                subtotal -= int(self.data_item.item(row,4).text())
                discount -= int(self.data_item.item(row,3).text())
                if int(self.data_item.item(row,2).text()) == 1:
                    self.data_item.removeRow(row)
                else:
                    qty = int(self.data_item.item(row,2).text()) - 1
                    self.data_item.setItem(row, 2, QtWidgets.QTableWidgetItem(str(qty)))    
        total = subtotal - discount
        self.display_bill(subtotal,discount,total)

    
    def scan(self):
        with open('data-cart.csv',mode= 'r') as csv_file:
            data_cart = csv.DictReader(csv_file, delimiter=",")
            line_count = self.data_item.rowCount()
            if len(self.subtotal_num.toPlainText()) > 0:   
                subtotal = int(self.subtotal_num.toPlainText())
                discount = int(self.discount_num.toPlainText())
            else:
                subtotal = 0
                discount = 0
            temp = True
            for data in data_cart:
                with open(r'Data\database-product.csv', mode= 'r') as csv_database:
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
                                    discount += int(row['discount'])*int(data['Qty'])
                                    temp = False
                            if temp:    
                                self.data_item.insertRow(line_count)
                                self.data_item.setItem(line_count, 1, QtWidgets.QTableWidgetItem(data['product_name']))
                                self.data_item.setItem(line_count, 2, QtWidgets.QTableWidgetItem(data['Qty']))
                                self.data_item.setItem(line_count, 0, QtWidgets.QTableWidgetItem(row['product_code']))
                                self.data_item.setItem(line_count, 3, QtWidgets.QTableWidgetItem(row['discount']))
                                self.data_item.setItem(line_count, 4, QtWidgets.QTableWidgetItem(row['product_price']))    
                                subtotal += int(data['Qty'])*int(row['product_price'])
                                discount += int(data['Qty'])*int(row['discount'])
                                line_count += 1
                        
        # print(subtotal)
        total = subtotal - discount
        self.display_bill(subtotal,discount,total)
    
    def pay(self):
        now = QDateTime.currentDateTime()
        with open(r'Data\invoice.csv', mode= 'a', newline='') as csv_database:
            fieldnames = ['invoice', 'Date', 'Amount']
            writer = csv.DictWriter(csv_database, fieldnames=fieldnames)
            Amount = self.total_num.toPlainText()
            invoice = now.toString('yyMMdd')
            print(invoice)
            writer.writerow({'invoice': invoice, 'Date': now.toString(Qt.DefaultLocaleLongDate), 'Amount': Amount})
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
        self.subtotal_num.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    def display_discount(self,text):
        self.discount_num.append(str(text))
        self.discount_num.setAlignment(QtCore.Qt.AlignRight)
    def display_total(self,text):
        self.total_num.append(str(text))
        self.total_num.setAlignment(QtCore.Qt.AlignRight)

    def pending(self):
        with open(r'Data\pending.csv', mode= 'w', newline='') as csv_database:
            while self.data_item.rowCount() > 0:
                data_product = csv.writer(csv_database)
                data = self.data_item.item(0,0).text(), self.data_item.item(0,1).text(), self.data_item.item(0,2).text(), self.data_item.item(0,3).text(), self.data_item.item(0,4).text()
                data_product.writerow(data)
                self.data_item.removeRow(0)
        self.NewData()

    def cart_temp(self):
        subtotal = 0
        discount = 0
        with open(r'Data\pending.csv', mode= 'r') as csv_database:
            data_product = csv.reader(csv_database, delimiter=",")
            line_count = 0
            for row in data_product:
                self.data_item.insertRow(line_count)
                self.data_item.setItem(line_count, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                self.data_item.setItem(line_count, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                self.data_item.setItem(line_count, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                self.data_item.setItem(line_count, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                self.data_item.setItem(line_count, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                subtotal += int(row[2])*int(row[4])
                line_count =+ 1
        total = subtotal - discount
        self.display_bill(subtotal,discount,total)

    def gotologin(self):
        gotologin = Login()
        widget.addWidget(gotologin)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoinvoice(self):
        gotoinvoice = NewInvoice()
        widget.addWidget(gotoinvoice)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoinventory(self):
        gotoinventory = Inventory()
        widget.addWidget(gotoinventory)
        widget.setCurrentIndex(widget.currentIndex()+1)
        print(widget.currentIndex)

class NewInvoice(QMainWindow):
    def __init__(self):
        super(NewInvoice, self).__init__()
        loadUi("newinvoice.ui", self)
        hheader = self.data_item.horizontalHeader()
        hheader.setSectionResizeMode(QHeaderView.Stretch)

        now = QDateTime.currentDateTime()
        self.clock.setText(now.toString(Qt.DefaultLocaleLongDate))

        with open(r'Data\invoice.csv', mode= 'r') as csv_database:
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
        self.logout.clicked.connect(self.gotologin)
        self.home.clicked.connect(self.gotocashier)
        self.inventory.clicked.connect(self.gotoinventory)

    def scan(self):
        line_count = self.data_item.rowCount()
        with open(r'Data\invoice.csv', mode= 'r') as csv_database:
            data_product = csv.DictReader(csv_database, delimiter=",")
            for row in data_product:
                self.data_item.insertRow(line_count)
                self.data_item.setItem(line_count, 0, QtWidgets.QTableWidgetItem(row['invoice']))
                self.data_item.setItem(line_count, 1, QtWidgets.QTableWidgetItem(row['date']))
                self.data_item.setItem(line_count, 2, QtWidgets.QTableWidgetItem('Rp. ' + row['amount']))
                if int(row['amount']) < 500:
                    self.setbgr(line_count)

                line_count += 1

    def sidemenu(self):
        width = self.sidebar_ext.width()
        if width == 55:
            newWidth = 230
        else: 
            newWidth = 55
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
        #self.data_item.item(row,3).setBackground(QtGui.QColor(255,0,0))
        #self.data_item.item(row,4).setBackground(QtGui.QColor(255,0,0))
        pass

    def gotologin(self):
        gotologin = Login()
        widget.addWidget(gotologin)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotocashier(self):
        gotoCashier = Cashier()
        widget.addWidget(gotoCashier)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoinventory(self):
        gotoinventory = Inventory()
        widget.addWidget(gotoinventory)
        widget.setCurrentIndex(widget.currentIndex()+1)

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
        self.menu.clicked.connect(self.sidemenu)
        self.logout.clicked.connect(self.gotologin)
        self.home.clicked.connect(self.gotocashier)
        self.invoice.clicked.connect(self.gotoinvoice)        
    
    def sidemenu(self):
        width = self.sidebar_ext.width()
        if width == 55:
            newWidth = 230
        else: 
            newWidth = 55
        self.animation = QPropertyAnimation(self.sidebar_ext, b"maximumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()

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
    
    def gotologin(self):
        gotologin = Login()
        widget.addWidget(gotologin)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotocashier(self):
        gotoCashier = Cashier()
        widget.addWidget(gotoCashier)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoinvoice(self):
        gotoinvoice = NewInvoice()
        widget.addWidget(gotoinvoice)
        widget.setCurrentIndex(widget.currentIndex()+1)

if __name__== "__main__":
    app = QApplication(sys.argv)
    window = Login()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(window)
    widget.show()
    widget.setWindowTitle("Prototype UI Cashier")
    sys.exit(app.exec_())