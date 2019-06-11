from pathlib import Path
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
from PIL import ImageTk, Image
import os
import pickle

class App:
    def __init__(self, master):
        self.main = master
        
        self.carousel_config()
        
    def carousel_config(self):
        self.carousel_frame = tk.Frame(self.main, width = 200, height = 50)
        self.carousel_frame.pack()
        
        self.labels = []
        for i in range(0, 10):
            self.labels.append(tk.Label(self.carousel_frame, text = 'Label {}'.format(i), width = 50, height = 50))
            self.labels[i].grid(row = 0, column = i)
    
    
    
root = tk.Tk()
GUI = App(root)
root.mainloop()
root.destroy()
exit()