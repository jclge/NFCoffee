from pad4pi import rpi_gpio
import os
import time

def printKey(key):
    fd = open('/home/pi/HUB/HUB_NFC_2018/input', 'w') #Where the input is stored
    fd.write(key)
    if key == '#':
        fd.close()
        keypad.cleanup() #Needed to avoid any overwriting problem
        exit
    fd.close()

ROW_PINS = [26, 21, 20, 16] #G-Pins code on raspberry : lines
COL_PINS = [19, 13, 6] # : Columuns

KEYPAD = [['1', '2', '3'], #Whole Keypad
        ['4', '5', '6'],
        ['7', '8', '9'],
        ['*', '0', '#']]
factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
keypad.registerKeyPressHandler(printKey)

try:
    while(True):
        time.sleep(0.2) #Totally arbitary, could be 0.15 or 0.25 but doesn't work that well with 0.1
except:
    keypad.cleanup()
