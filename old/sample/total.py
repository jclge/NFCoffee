# coding: utf-8
import nfc
from datetime import datetime
import ndef
from pathlib2 import Path
from Tkinter import *
from time import clock
from time import sleep
import time
import subprocess
import os
import sys

uid = 0
temp = None
avrg = 0

def empty(root): #Exit card execution
    root.destroy()
    avrg = 1

def on_connect(tag): #Check if card on reader
    global uid
    uid = str(tag.identifier).encode("hex").upper()
    return True

def log(init, path, res): #Set trade in log
    date = datetime.now()
    if res == 0:
        fir = " + "
    else:
        fir = " - "
    s = path + fir + init
    fd = open('log', 'a')
    fd.write(str(date))
    fd.write("\n")
    fd.write(s)
    fd.write('\n')
    fd.close #Format : Date \n ID \n

def recharger(root, argv, path): #Set coffees on card 
    res = [''] * 5
    check = 0
    root.destroy()
    root = Tk()
    frame = Frame(root)
    frame.pack()
    subprocess.Popen(['sudo python3 file.py'], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True) #Potential memory leak (calls keypad)
    init = '0'
    t2 = Button(root, text="Recharger de :", height = 1, width = 19, fg = "#e8632b", bg = "black", activeforeground="#e8632b", activebackground="black", font="Arial 35 bold", cursor='none', command=None)
    t2.pack(side=TOP)
    t = Text(root, height = 5, width = 19, bg = "#e8632b", fg = "black", font = "Arial 40 bold", cursor='none')
    t.pack(side=BOTTOM)
    i = 0
    while(check != 1):
        fd = open('input', 'r+')
        string = fd.read()
        if string == '1' or string == '2' or string == '3' or string == '4' or string == '5' or string == '6' or string == '7' or string == '8' or string == '9' or string == '0' or string == '*' or string == '#':
            if string == '*' and i > 0:
                if  i == 3 and res[i] != '':
                    res[i] = ''
                else:
                    res[i - 1] = ''
                    i = i - 1
                    fd.truncate(0)
            elif string == '#':
                fd.truncate(0)
                i = 0
                fd.close()
                fd = open(path, 'r')
                string = fd.read()
                calc = int(string) + int(init)
                fd.close()
                fd = open(path, 'w')
                fd.write(str(calc))
                fd.close()
                fd = open('input', 'w')
                fd.truncate(0)
                fd.close()
                root.destroy()
                if init != '' and init != None and init != '0':
                   conf(calc, init, 0)
                   log(init, path, 0)
                check = 1
            elif string == '*' and i == 0:
                res[i] = ''
                fd.truncate(0)
            else:
                res[i] = string
                fd.truncate(0)
                if i != 3:
                    i = i + 1
            init = None
            init = ''.join(res)
            if check != 1:
                t.delete('1.0', END)
                t.insert(INSERT, init)
        if check != 1:
            fd.close()
            root.attributes("-fullscreen", True)
            sleep(0.1)
            root.after(15000, lambda: empty(root))
            root.update()

def switch(argv, root, frame): #Go back on main menu when card is read
    root.destroy()
    root = Tk()
    button(argv, root, frame)

def conf(calc, init, res): #Confirmation
    root = Tk()
    frame = Frame(root)
    frame.pack()
    t = Text(root, height=50, width=50, fg="#e8632b", bg="black", font="Arial 30 bold", cursor='none')
    t.pack(side=TOP)
    if int(init) > 1:
        fir = "s"
    else:
        fir = ""
    if calc > 1:
        sec = "s"
    else:
        sec = ""
    if (res == 1):
        s = "Carte bien debitée de \n" + init + " café" + fir + " !\n" + str(calc) + " café" + sec +" restant" + sec + "."
    else:
        s = "Carte bien rechargée de \n" + init + " café" + fir + " !\n" + str(calc) + " café" + sec + " au total."
    t.insert(INSERT, s)
    root.attributes("-fullscreen", True)
    if (res == 0):
        root.after(5000, lambda: switch(str(calc), root, frame))
    else:
        root.after(5000, lambda: empty(root))
    if (avrg != 1):
        root.mainloop()

def debiter(root, argv, path): #Delete coffees from card
    check = 0
    abs = 0
    res = [''] * 5
    root.destroy()
    root = Tk()
    frame = Frame(root)
    frame.pack()
    subprocess.Popen(['sudo python3 file.py'], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True) #Potential memory leak (calls keypad)
    init = '0'
    t1 = Button(root, text="Débiter de :", height = 1, width = 19, fg = "#e8632b", bg = "black", activeforeground="#e8632b", activebackground="black", font = "Arial 35 bold", cursor='none')
    t1.pack(side=TOP)
    t = Text(root, height = 5, width = 19, bg = "#e8632b", fg = "black", font = "Arial 40 bold", cursor='none')
    t.pack(side=BOTTOM)
    i = 0
    while(check != 1):
        abs = 0
        fd = open('input', 'r+')
        string = fd.read()
        if string == '1' or string == '2' or string == '3' or string == '4' or string == '5' or string == '6' or string == '7' or string == '8' or string == '9' or string == '0' or string == '*' or string == '#':
            if string == '*' and i > 0:
                if  i == 3 and res[i] != '':
                    res[i] = ''
                else:
                    res[i - 1] = ''
                    i = i - 1
                fd.truncate(0)
            elif string == '#':
                fd.truncate(0)
                print init
                if init != '' and init != 'Pas assez de cafes sur la carte' and init != None:
                    if int(init) > int(argv):
                        res[1] = ''
                        res[2] = ''
                        res[3] = ''
                        res[0] = 'Pas assez de \ncafés sur la carte'
                        init = None
                        init = ''.join(res)
                        t.delete('1.0', END)
                        t.insert(INSERT, init)
                        root.update_idletasks()
                        sleep(1)
                        res[0] = '0'
                        i = 0
                        abs = 1
                        subprocess.Popen(['sudo python3 file.py'], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True) #Potential memory leak
                if abs != 1:
                    fd.truncate(0)
                    i = 0
                    fd.close()
                    root.destroy()
                    if init != None and init != '' and init != '0':
                        fd = open(path, 'r')
                        string = fd.read()
                        calc = int(string) - int(init)
                        fd.close()
                        fd = open(path, 'w')
                        fd.write(str(calc))
                        fd.close()
                        conf(calc, init, 1)
                        log(init, path, 1)
                        fd = open('input', 'w')
                        fd.truncate(0)
                        fd.close()
                    check = 1
            elif string == '*' and i == 0:
                res[i] = ''
                fd.truncate(0)
            else:
                res[i] = string
                fd.truncate(0)
                if i != 3:
                    i = i + 1
            init = None
            init = ''.join(res)
            if check != 1:
                t.delete('1.0', END)
                t.insert(INSERT, init)
        if check != 1:
            fd.close()
            root.attributes("-fullscreen", True)
            sleep(0.1)
            root.after(15000, lambda: empty(root))
            root.update()

def go_back(path, root): #After switch()
    root.destroy()
    root = Tk()
    frame = Frame(root)
    frame.pack()
    fd = open(path)
    res = fd.read()
    button(res, root, frame)

def log_hist(path, root): #Print last 12 trades on a card
	root.destroy()
    root = Tk()
    i = 0
    y = 0
    u = 0
    res = [''] * 12
    temp = [''] * 30
    temp_date = [''] * 30
    fd = open('log')
    rode = fd.read()
    trs = [''] * len(rode)
    while i != len(rode):
        if (rode[i] == None or rode[i] == '\n' or rode[i] == ' '):
            trs[y] = '$'
            y += 1
            i += 1
        else:
            trs[y] = rode[i]
            y += 1
            i+= 1
    y = 0
    i = 0
    rode = ''.join(trs)
    while i != len(rode):
        if rode[i] == '2' and rode[i + 1] == '0' and rode[i + 4] == '-':
            while rode[i] != '.':
                temp_date[y] = rode[i]
                y += 1
                i += 1
            y = 0
            temp_date[10] = ' '
            i += 8
            while rode[i] != '$':
                temp[y] = rode[i]
                y += 1
                i += 1
            y = 0
            if ''.join(temp) == path:
                if u == 12:
                    while y != 11:
                        res[y] = res[y + 1]
                        y += 1
                    u = 11
                    y = 0
		if rode[i + 4] != '$':
                    res[u] = ''.join(temp_date) + rode[i + 1] + rode[i + 3] + rode[i + 4] + '\n'
                else:
                    res[u] = ''.join(temp_date) + rode[i + 1] + rode[i + 3] + '\n'
                u += 1
        i += 1
    init = ''.join(res)
    t = Text(root, height=12, width=200, bg='#e8632b', fg='black', font='Arial 15 bold', cursor='none')
    t.pack(side=TOP)
    t.insert(INSERT, str(init))
    B8 = Button(root, fg='black', bg='#e8632b', activeforeground='#e8632b', activebackground='black', cursor='none', text='Retour', font='Arial 40 bold', height=2, width=20, command=lambda: go_back(path, root))
    B8.pack(side=BOTTOM)
    root.attributes('-fullscreen', True)
    root.mainloop()

def button(argv, root, frame): #Main menu when card read
    t = Text(root, height = 1, width = 17, bg = "#e8632b", fg = "black", font = "Arial 40 bold", cursor='none')
    t.pack(side=TOP)
    if argv != '0':
        res = 9
    else:
        res = 20
    if int(argv) > 1:
        fir = "s"
    else:
        fir = ""
    s = " " + argv + " café" + fir + " restant" + fir
    t.insert(INSERT, s)
    B2 = Button(root,
                fg='black',
                bg='#e8632b',
                activeforeground='#e8632b',
                activebackground='black',
                font='Arial 25 bold',
                width=27,
                height=1,
                text='Annuler',
                cursor='none',
                command = lambda : empty(root))
    B2.pack(side=BOTTOM)
    B3 = Button(root,
               fg='black',
               bg='#e8632b',
               activeforeground='#e8632b',
               activebackground='black',
               font='Arial 25 bold',
               width=27,
               height=1,
               text='Historique',
               cursor='none',
               command= lambda: log_hist(path, root))
    B3.pack(anchor='s')
    B = Button(root,
               fg='black',
               bg='#e8632b',
               activeforeground='#e8632b',
               activebackground='black',
               font='Arial 35 bold',
               width=res,
               height=4,
               text ="Recharger",
               cursor='none',
               command = lambda: recharger(root, argv, path))
    B.pack(side=LEFT)
    if argv != '0':
        B1 = Button(root,
                    fg='black',
                    bg='#e8632b',
                    activeforeground='#e8632b',
                    activebackground='black',
                    font='Arial 35 bold',
                    width=100,
                    height=4,
                    text ="Débiter",
                    cursor='none',
                    command = lambda: debiter(root, argv, path))
        B1.pack(side=LEFT)
    if avrg != 1:
        root.attributes("-fullscreen", True)
        root.after(15000, lambda: empty(root))
        root.mainloop()

rdwr_options = {
    'on-connect': on_connect,
    'beep-on-connect': True,
}
f_exist = 0
sleep(7) #To let the NFC start and avoiding cron doing it
subprocess.Popen(['sudo python image.py'], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
while True: #Main Loop
    with nfc.ContactlessFrontend('usb') as clf:
        tag = clf.connect(rdwr=rdwr_options)
    if (uid != 0):
        path = "../DB_HUB/" + uid
    my_file = Path(path)
    if my_file.is_file():
        fd = open(path, 'r')
    else:
        fd = open(path, 'w+')
        fd.write("0")
        fd.close()
        fd = open(path, 'r')
    res = fd.read()
    root = Tk()
    frame = Frame(root)
    frame.pack()
    button(res, root, frame)
    avrg = 0
    uid = 0
