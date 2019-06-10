import tkinter as tk
from PIL import Image
import os

root = tk.Tk()

mb =  tk.Menubutton(root, text="CheckComboBox", relief=tk.RAISED )
mb.pack()
mb.menu  =  tk.Menu(mb, tearoff = 0 )
mb["menu"]  =  mb.menu

pcwd = os.path.dirname(os.getcwd())
iconpath = '{}\\assets\\Icon Pack\\small'.format(pcwd)

BT1 = tk.PhotoImage(file = '{}\\BT-small.png'.format(iconpath))
BR1 = tk.PhotoImage(file = '{}\\BR-small.png'.format(iconpath))
SW1 = tk.PhotoImage(file = '{}\\SW-small.png'.format(iconpath))

icons = [BT1, BR1, SW1]

for i in range(0,3):
    mb.menu.add_command(label="", image=icons[i], compound="left")


mb.pack()
root.mainloop()
