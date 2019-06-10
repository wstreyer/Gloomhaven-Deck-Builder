import tkinter as tk
from PIL import Image
import os

def select_class(ghclass):
    print(ghclass)

root = tk.Tk()

mb =  tk.Menubutton(root, text="Class", relief=tk.RAISED )
mb.pack()
mb.menu  =  tk.Menu(mb, tearoff = 0 )
mb["menu"]  =  mb.menu

pcwd = os.path.dirname(os.getcwd())
iconpath = '{}\\assets\\Icon Pack\\full'.format(pcwd)

w = 30
h = 30

icons = {}
for icon in os.listdir(iconpath):
    name = icon.split('.')[0]
    img = Image.open('{}\\{}'.format(iconpath, icon))
    img = img.resize((w,h), Image.ANTIALIAS)
    imgfile = '{}\\assets\\Icon Pack\\small\\{}-small.png'.format(pcwd, name) 
    img.save(imgfile)
    icons[name] = tk.PhotoImage(file = imgfile)

for icon in icons:
    mb.menu.add_command(label='', image=icons[icon], compound="left", command = lambda my_icon = icon: select_class(my_icon))

mb.pack()
root.mainloop()
