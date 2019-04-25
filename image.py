from Tkinter import *
from PIL import Image, ImageTk
import os
from time import sleep

def mansd(): #Put an Image in background to avoid any pop-up/info to show up on the screen
    root = Tk()
    img = ImageTk.PhotoImage(Image.open("bg_NFCoffee.png"))
    panel = Label(root, image = img)
    panel.pack(side = "bottom", fill='both', expand = "yes")
    panel.config(cursor="none")
    root.attributes("-fullscreen", True)
    root.mainloop()

mansd()
