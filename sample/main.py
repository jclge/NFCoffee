# coding: utf-8
import nfc
from datetime import datetime
import base64
from time import sleep
import time
import subprocess
import os
import codecs
import sys
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from pathlib2 import Path
import sys
import MySQLdb as mc
import datetime

uid = 0
width = 1920
height = 1080
connection = 0
cursor = 0
nb = 0

def coffee_nb(tmp):
    return (int(tmp[0][0]))

def connect():
    global uid, cursor, connection
    connection = mc.connect (host = "sql2.freesqldatabase.com",
                            user = "sql2321646",
                            passwd = "",
                            db = "sql2321646")

    cursor = connection.cursor()

def create_card():
    global uid, cursor, connection
    date_object = str(datetime.date.today())
    staff_data = [ (0, uid, date_object, "creation"),
                ]

    for staff, p in enumerate(staff_data):
        format_str = """INSERT INTO coffee (id, coffee, card, date, historic)                                                                                                                       
        VALUES ({id}, {coffee}, "{card}", "{date}", "{historic}");"""
        sql_command = format_str.format(id=staff, coffee=p[0], card=p[1], date=p[2], historic=p[3])
        print(sql_command)
        cursor.execute(sql_command)
    connection.commit()
    return

class App_empty(QMainWindow, QWidget):
    global uid, width, height
    def __init__(self):
        super().__init__()
        self.title = 'NFCoffee'
        self.left = 10
        self.top = 10
        self.width = width
        self.height = height
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage("NFCoffee'")
        self.setStyleSheet("background-color: black")
        self.textbox = QLineEdit(self)
        self.textbox.move(0, 0)
        self.textbox.resize(width/2, height/4)
        self.textbox.setReadOnly(True)
        self.textbox.setText('Aucun café restant')
        self.textbox.setStyleSheet("background-color: white; font-size: 36px")
        button_r = QPushButton('RECHARGER', self)
        button_r.setStyleSheet("background-color: orange; font-size: 36px")
        button_r.resize(width,(height/4)*3-height/10)
        button_r.move(0,height/4)
        button_r.clicked.connect(self.on_click)
        button_t = QPushButton('Historique', self)
        button_t.setStyleSheet("background-color: orange; font-size: 26px")
        button_t.resize(width/2,height/4)
        button_t.move(width/2,0)
        button_t.clicked.connect(self.historic)

        button_s = QPushButton('Annuler', self)
        button_s.setStyleSheet("background-color: orange; font-size: 26px")
        button_s.resize(width,height/10)
        button_s.move(0,(height/10)*9)
        button_s.clicked.connect(self.cancel)
        self.showFullScreen()

    @pyqtSlot()
    def cancel(self):
        self.close()

    @pyqtSlot()
    def on_click(self):
        self.statusBar().showMessage("Switched to window 1")
        self.cams = Window1("2hcejhd") 
        self.cams.show()
        self.close()

    @pyqtSlot()
    def historic(self):
        self.statusBar().showMessage("Switched to window 1")
        self.cams = Window3() 
        self.cams.show()
        self.close()

class Window1(QDialog):
    global width, height, nb, uid, cursor, connection
    def __init__(self, value, parent=None):
        super().__init__()
        self.title = 'NFCoffee'
        self.total = 0
        self.left = 10
        self.top = 10
        self.width = width
        self.height = height
        self.initUI()

    @pyqtSlot()
    def rld(self):
        print('Exiting')
        exit()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color: black")

        button_r = QPushButton('-11', self)
        button_r.setStyleSheet("background-color: orange; font-size: 36px")
        button_r.resize(width/5,height/2)
        button_r.move(0,0)
        button_r.clicked.connect(self.minus_11)

        button_s = QPushButton('-1', self)
        button_s.setStyleSheet("background-color: orange; font-size: 36px")
        button_s.resize(width/5,height/2)
        button_s.move(width/5,0)
        button_s.clicked.connect(self.minus_1)

        self.textbox = QLineEdit(self)
        self.textbox.move(width/5*2, 0)
        self.textbox.resize(width/5,height/2)
        self.textbox.setReadOnly(True)
        self.textbox.setText(str(nb))
        self.textbox.setStyleSheet("background-color: white; font-size: 156px; float: center")

        button_t = QPushButton('+10', self)
        button_t.setStyleSheet("background-color: orange; font-size: 36px")
        button_t.resize(width/5,height/2)
        button_t.move((width/5)*3,0)
        button_t.clicked.connect(self.plus_10)

        button_u = QPushButton('+11', self)
        button_u.setStyleSheet("background-color: orange; font-size: 36px")
        button_u.resize(width/5,height/2)
        button_u.move((width/5)*4,0)
        button_u.clicked.connect(self.plus_11)

        button_v = QPushButton('Confirmer', self)
        button_v.setStyleSheet("background-color: orange; font-size: 36px")
        button_v.resize(width,height/10*4)
        button_v.move(0,height/2)
        button_v.clicked.connect(self.addcoffee)

        button_w = QPushButton('Annuler', self)
        button_w.setStyleSheet("background-color: orange; font-size: 36px")
        button_w.resize(width,height/10)
        button_w.move(0,height/10*9)
        button_w.clicked.connect(self.on_click)
        self.showFullScreen()

    @pyqtSlot()
    def on_click(self):
        self.close()

    @pyqtSlot()
    def minus_11(self):
        tmp = int(self.textbox.text())
        if (tmp - 11 < int(nb)):
            tmp = int(nb)
            self.total = 0
        else:
            tmp -= 11
            self.total += 11
        self.textbox.setText(str(tmp))

    def minus_1(self):
        tmp = int(self.textbox.text())
        if (tmp - 1 < int(nb)):
            tmp = int(nb)
            self.total = 0
        else:
            tmp -= 1
            self.total -= 1
        self.textbox.setText(str(tmp))

    @pyqtSlot()
    def plus_11(self):
        tmp = int(self.textbox.text())
        tmp += 11
        self.total += 11
        self.textbox.setText(str(tmp))
    
    @pyqtSlot()
    def addcoffee(self):
        res = "SELECT historic FROM coffee WHERE card ='" + uid + "';"
        cursor.execute(res)
        historic = str(cursor.fetchall()[0][0])
        connection.commit()
        tmp = int(self.textbox.text())
        strd = """UPDATE coffee SET coffee =""" + str(tmp) + """ WHERE card ='""" + uid + "';"""
        cursor.execute(strd)
        connection.commit()
        date_object = str(datetime.date.today())
        strd2 = """UPDATE coffee SET date='""" + date_object + """' WHERE card ='""" + uid + "';"""
        cursor.execute(strd2)
        connection.commit()
        strd3 = """UPDATE coffee SET historic ='+""" + str(self.total) + ' (=' + str(tmp) +');' + historic + """' WHERE card ='""" + uid + "';"""
        cursor.execute(strd3)
        connection.commit()
        self.close()
    
    @pyqtSlot()
    def plus_10(self):
        tmp = int(self.textbox.text())
        tmp += 10
        self.total += 10
        self.textbox.setText(str(tmp))

class Window2(QDialog):
    global width, height, nb, uid, cursor, connection
    def __init__(self, value, parent=None):
        super().__init__()
        self.title = 'NFCoffee'
        self.left = 10
        self.top = 10
        self.width = width
        self.total = 0
        self.height = height
        self.initUI()

    @pyqtSlot()
    def rld(self):
        print('Exiting')
        exit()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color: black")
        button_s = QPushButton('+1', self)
        button_s.setStyleSheet("background-color: orange; font-size: 36px")
        button_s.resize(width/3,height/2)
        button_s.move(0,0)
        button_s.clicked.connect(self.plus_1)
        self.textbox = QLineEdit(self)
        self.textbox.move(width/3, 0)
        self.textbox.resize(width/3,height/2)
        self.textbox.setReadOnly(True)
        self.textbox.setText(str(nb))
        self.textbox.setStyleSheet("background-color: white; font-size: 156px; float: center")
        button_u = QPushButton('-1', self)
        button_u.setStyleSheet("background-color: orange; font-size: 36px")
        button_u.resize(width/3,height/2)
        button_u.move((width/3*2),0)
        button_u.clicked.connect(self.minus_1)
        button_v = QPushButton('Confirmer', self)
        button_v.setStyleSheet("background-color: orange; font-size: 36px")
        button_v.resize(width,4*(height/10))
        button_v.move(0,height/2)
        button_v.clicked.connect(self.addcoffee)
        button_w = QPushButton('Annuler', self)
        button_w.setStyleSheet("background-color: orange; font-size: 36px")
        button_w.resize(width,height/10)
        button_w.move(0,(height/10)*9)
        button_w.clicked.connect(self.on_click)
        self.showFullScreen()

    @pyqtSlot()
    def on_click(self):
        self.close()

    @pyqtSlot()
    def plus_1(self):
        tmp = int(self.textbox.text())
        if (tmp + 1 > int(nb)):
            tmp = int(nb)
            self.total = 0
        else:
            tmp += 1
            self.total -= 1
        self.textbox.setText(str(tmp))

    def plus_2(self):
        tmp = int(self.textbox.text())
        if (tmp + 2 > int(nb)):
            tmp = int(nb)
        else:
            tmp += 2
        self.textbox.setText(str(tmp))

    @pyqtSlot()
    def minus_1(self):
        tmp = int(self.textbox.text())
        if (tmp - 1 < 0):
            tmp = 0
        else:
            tmp -= 1
            self.total += 1
        self.textbox.setText(str(tmp))

    @pyqtSlot()
    def minus_2(self):
        tmp = int(self.textbox.text())
        if (tmp - 2 < 0):
            tmp = 0
        else:
            tmp -= 2
        self.textbox.setText(str(tmp))
    
    @pyqtSlot()
    def addcoffee(self):
        res = "SELECT historic FROM coffee WHERE card ='" + uid + "';"
        cursor.execute(res)
        historic = str(cursor.fetchall()[0][0])
        connection.commit()
        tmp = int(self.textbox.text())
        strd = """UPDATE coffee SET coffee =""" + str(tmp) + """ WHERE card ='""" + uid + "';"""
        cursor.execute(strd)
        connection.commit()
        date_object = str(datetime.date.today())
        strd2 = """UPDATE coffee SET date='""" + date_object + """' WHERE card ='""" + uid + "';"""
        cursor.execute(strd2)
        connection.commit()
        strd3 = """UPDATE coffee SET historic ='-""" + str(self.total) + ' (=' + str(tmp) +');' + historic + """' WHERE card ='""" + uid + "';"""
        cursor.execute(strd3)
        connection.commit()
        self.close()

class App(QMainWindow, QWidget):
    global uid, width, height, nb
    def __init__(self):
        super().__init__()
        self.title = 'NFCoffee'
        self.left = 10
        self.top = 10
        self.width = width
        self.height = height
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage("NFCoffee'")
        self.setStyleSheet("background-color: black")
        self.textbox = QLineEdit(self)
        self.textbox.move(0, 0)
        self.textbox.resize(width/2, height/4)
        self.textbox.setReadOnly(True)
        if (int(nb) > 1):
            self.textbox.setText(str(nb) + ' cafés restants')
        elif (int(nb) == 1):
            self.textbox.setText(str(nb) + ' café restant')
        else:
            self.textbox.setText('Aucun café restant')
        self.textbox.setStyleSheet("background-color: white; font-size: 64px; float: center")
        button_r = QPushButton('RECHARGER', self)
        button_r.setStyleSheet("background-color: orange; font-size: 36px")
        button_r.resize(width/2,(height/4)*3-height/10)
        button_r.move(0,height/4)
        button_r.clicked.connect(self.on_click)
        button_d = QPushButton('DEBITER', self)
        button_d.setStyleSheet("background-color: orange; font-size: 36px")
        button_d.resize(width/2,(height/4)*3-height/10)
        button_d.move(width/2,height/4)
        button_d.clicked.connect(self.on_click_d)
        button_s = QPushButton('Annuler', self)
        button_s.setStyleSheet("background-color: orange; font-size: 26px")
        button_s.resize(width,height/10)
        button_s.move(0,(height/10)*9)
        button_s.clicked.connect(self.cancel)
        button_t = QPushButton('Historique', self)
        button_t.setStyleSheet("background-color: orange; font-size: 26px")
        button_t.resize(width/2,height/4)
        button_t.move(width/2,0)
        button_t.clicked.connect(self.historic)
        self.showFullScreen()

    @pyqtSlot()
    def on_click(self):
        self.statusBar().showMessage("Switched to window 1")
        self.cams = Window1("2hcejhd") 
        self.cams.show()
        self.close()

    @pyqtSlot()
    def historic(self):
        self.statusBar().showMessage("Switched to window 1")
        self.cams = Window3() 
        self.cams.show()
        self.close()

    @pyqtSlot()
    def cancel(self):
        self.close()

    @pyqtSlot()
    def on_click_d(self):
        self.statusBar().showMessage("Switched to window 2")
        self.cams = Window2("2hcejhd") 
        self.cams.show()
        self.close()

class Window3(QScrollArea):
    global nb, connection, cursor, uid
    def __init__(self):
        super().__init__()
        self.title = 'NFCoffee'
        self.left = 10
        self.top = 10
        self.width = width
        self.height = height
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color: black")
        self.textbox = QLabel(self)
        self.textbox.move(0, height/10)
        self.textbox.resize(width, height-height/10)
        self.textbox.setWordWrap(True)
        res = "SELECT historic FROM coffee WHERE card ='" + uid + "';"
        cursor.execute(res)
        tmp = cursor.fetchall()
        tmp = tmp[0][0].replace(';', '\n')
        tmp = '\n' + tmp
        res2 = "SELECT date FROM coffee WHERE card ='" + uid + "';"
        cursor.execute(res2)
        tmp2 = cursor.fetchall()
        res3 = "La dernière opération est datée de: " + str(tmp2[0][0])
        button_r = QPushButton(res3, self)
        button_r.setStyleSheet("background-color: orange; font-size: 36px")
        button_r.resize(width,height/10)
        button_r.move(0,0)
        button_r.clicked.connect(self.on_click)
        self.textbox.setText(tmp)
        self.textbox.setStyleSheet("background-color: white; font-size: 35px; margin-top: 3px")
        button_r = QPushButton('Retour', self)
        button_r.setStyleSheet("background-color: orange; font-size: 36px")
        button_r.resize(width,height/10)
        button_r.move(0,height/10*9)
        button_r.clicked.connect(self.on_click)
        self.showFullScreen()

    @pyqtSlot()
    def on_click(self):
        if (int(nb) > 0):
            self.cams = App() 
        else:
            self.cams = App_empty()
        self.cams.show()
        self.close()

def on_connect(tag):
    global uid
    uid = str(codecs.encode(tag.identifier, 'hex').upper())
    return True


def main():
    global uid, width, height, connection, cursor, nb
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    width = rect.width()
    height = rect.height()
    rdwr_options = {
        'on-connect': on_connect,
        'beep-on-connect': False,
    }
    connect()

    while True: #Main Loop
        with nfc.ContactlessFrontend('usb') as clf:
            clf.connect(rdwr=rdwr_options)
        if (uid != "0"):
            uid = uid.replace("'", '')
            uid = uid.replace('b', '')
            res = "SELECT coffee FROM coffee WHERE card ='" + uid + "';"
            cursor.execute(res)
            tmp = cursor.fetchall()
            if (len(tmp) == 0):
                create_card()
                nb = '0'
                ex = App_empty()
                app.exec_()
            elif (tmp[0][0] == 0):
                nb = '0'
                ex = App_empty()
                app.exec_()
            else:
                nb = str(tmp[0][0])
                ex = App()
                app.exec_()
        uid = "0"
        
if __name__ == "__main__":
    main()
