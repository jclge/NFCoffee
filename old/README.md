### NFCoffee

Here is a simple Python 2.7 program to read NFC tags on cards to manage coffees on a local database.

### Features

    -Read a NFC card.
    -Display with Tkinter the number of coffee left.
    -Let the user set as many coffee as he wants on the card (up to 9999 at once).
    -Display a log history of each card.

### Librairies build

```bash
~$ pip install nfcpy
~$ pip3 install pad4pi
~$ pip install pillow
~$ pip install pathlib2
~$ pip install tkinter
~$ git clone https://github.com/mdeverdelhan/ACR122U-reader-writer.git / OR whatever you will need for your NFC reader/writer
```
Potential librairies for a GPin-connected screen

### Usage

```bash
~$ sudo python total.py
```
### Device features

       A Raspberry pi 3 or above.
       Or an Arduino able to do the same.
       A screen (at least 2.5 inch to keep it user friendly).
       A NFC reader, here we have used the ACR 122U.
       A 3*4 matrix keypad with 7 dupont connectors.
       It could work perfectly with a 4*4 matrix or simply a laptop/computer. 

### Notes

It has been done for a project in Epitech Lyon, to make the coffee transactions easier inside the Student Union "Zero To One" and nexts.
It will probably need many modifications to adapt on your device and/or software.

\ Halil Bagdadi & Julien Calenge /
