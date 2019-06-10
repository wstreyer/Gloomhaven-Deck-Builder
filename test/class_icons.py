import os
import pdf2image
import tkinter as tk

#Extract image
pcwd = os.path.dirname(os.getcwd())
pdfpath = '{}\\assets\\Icon Pack'.format(pcwd)
pdffile = '{}\\Class Icons and Augments.pdf'.format(pdfpath)
icons = pdf2image.convert_from_path(pdffile, dpi = 150, fmt='png')

#Save the icon images
names = {1:'BT',
         2:'', 
         3:'BR', 
         4:'', 
         5:'', 
         6:'MT', 
         7:'', 
         8:'', 
         9:'SW', 
         10:'', 
         11:'', 
         12:'TI', 
         13:'', 
         14:'SC', 
         15:'', 
         16:'', 
         17:'CH', 
         18:'', 
         19:'', 
         20:'', 
         21:'', 
         22:'', }
for n, icon in enumerate(icons):
    if names[n+1] == '':
        name = n+1
    else:
        name = names[n+1]
    icon.save('{}\{}.{}'.format(pdfpath, name, 'png'))

root = tk.Tk()

mb =  tk.Menubutton(root, text="CheckComboBox", relief=tk.RAISED )
mb.pack()
mb.menu  =  tk.Menu(mb, tearoff = 0 )
mb["menu"]  =  mb.menu

mb.pack()
root.mainloop()