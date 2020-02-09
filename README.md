### NFCoffee

Here is a simple Python 3.6+ program to read NFC tags on cards to manage coffees on a distant database.

### Features

    -Read a NFC card.
    -Display with QT5 the number of coffee left.
    -Let the user set as many coffee as he wants on the card.
    -Display a log history of each card.

### Librairies build

```bash
~$ pip install nfcpy
~$ pip install pathlib2
```

### Usage

```bash
~$ sudo python total.py
```
### Device features

       A NFC reader, here we have used the ACR 122U.
       The design is made to work properly with a Raspberry 3B+ with a standard 2.5" screen.

### Notes

We are using freesqldatabase.com to host the database. The free version allows up to 50MB of data, which represents about 3000 rows in our configuration.
It has been done for a project in Epitech Lyon, to make the coffee transactions easier inside the Student Union "Zero To One" and nexts.
It should not be hard to adapt to your devices and/or databases.
You can add a pad pretty easily with the library "pad4pi" but this modification includes modifying a wide part of the program.

\ Halil Bagdadi & Julien Calenge /
