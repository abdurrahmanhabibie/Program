from PyQt5.QtCore import QDateTime, Qt
from reportlab.pdfgen import canvas
import qrcode

data = [
    ['Nextar blueberry', '2', '8000'],
    ['Oreo Vanila', '4', '2000'],
    ['Ayam Bawang', '3', '2500'],
]

now = QDateTime.currentDateTime()

invoice = now.toString('yyMMdd-HHmm-ss')
Axis = 220 +(len(data)*10)
# Creating Canvas
path = "Invoice/{}.pdf".format(invoice)
c = canvas.Canvas(path,pagesize=(200,Axis),bottomup=0)
# Logo Section
# Setting th origin to (10,40)
c.translate(10,40)
# Inverting the scale for getting mirror Image of logo
c.scale(1,-1)
# Inserting Logo into the Canvas at required position
c.drawImage("file/logo.jpg",0,0,width=50,height=30)
# Title Section
# Again Inverting Scale For strings insertion
c.scale(1,-1)
# Again Setting the origin back to (0,0) of top-left
c.translate(-10,-40)
# Setting the font for Name title of company
c.setFont("Helvetica-Bold",10)
# Inserting the name of the company
c.drawCentredString(125,20,"Prototipe Cetak Invoice")
# For under lining the title
c.line(70,22,180,22)
# Changing the font size for Specifying Address
c.setFont("Helvetica-Bold",7)
c.drawCentredString(125,30,"Jl. Sangkuriang No.15 - 40135")
c.drawCentredString(125,38,"Dago - Bandung")
# Changing the font size for Specifying GST Number of firm
# Line Seprating the page header from the body
c.line(5,45,195,45)
c.setFont("Helvetica-Bold",6)
now = QDateTime.currentDateTime()
c.drawString(5,55,"Date/Time   : " + now.toString(Qt.DefaultLocaleLongDate))
c.drawString(5,62,"Invoice No. : {}".format(invoice))
c.line(5,67,195,67)
c.setFont("Courier-Bold",7)
count = 0
Y = 77
harga = 0
diskon = 1700
for row in data:
    subtotal = int(data[count][1]) * int(data[count][2])
    
    c.drawString(10, Y, str(data[count][0]))
    c.drawRightString(100,Y,str(data[count][1]))
    c.drawRightString(140,Y,str(data[count][2]))
    c.drawRightString(190,Y,str(subtotal))
    harga = harga + int(subtotal)
    count +=1
    Y += 7
Y = 77 + (count*7) - 2
c.line(90,Y,195,Y)

c.drawString(90,Y+10,"Subtotal :")
c.drawRightString(190,Y+10,str(harga))
c.drawString(90,Y+20,"Discount :")
c.drawRightString(190,Y+20,str(diskon))
c.line(90,Y+25,195,Y+25)

total = harga - diskon
c.drawString(90,Y+35,"Total    :")
c.drawRightString(190,Y+35,str(total))

money = total
c.drawString(90,Y+45,"E-money  :")
c.drawRightString(190,Y+45,str(money))

change = money - total
c.drawString(90,Y+55,"Change   :")
c.drawRightString(190,Y+55,str(change))

c.line(5,Y+60,195,Y+60)
c.drawCentredString(100,Y+70,"Thank you for visiting")

qr = qrcode.make(data)
qr.save('Data/myQr.jpg')
c.drawImage("Data/myQr.jpg",65,Y+80,width=70,height=70)

c.showPage()
# Saving the PDF
c.save()