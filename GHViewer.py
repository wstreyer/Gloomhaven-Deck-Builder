# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:41:31 2019

@author: InnSight
"""

import urllib.request
import pdf2image
import tkinter as tk
from PIL import ImageTk, Image
import time

resourceurl = 'https://drive.google.com/uc?export=download&id='

resources = {'BR':'0B8ppELln5Z0rdjJzSGZMYXNqVkE',
             'CH':'0B8ppELln5Z0raUNvY3BNbG1adjQ',
             'MT':'0B8ppELln5Z0rdFBmMFdkTXhLZ1U',
             'SC':'0B8ppELln5Z0rbTlRLUIxVk5NQlE',
             'SW':'0B8ppELln5Z0rYjhYQkV4bUpoOFE',
             'TI':'0B8ppELln5Z0rUVJRRGw1MTV5cTQ',
             'BT':'0B8ppELln5Z0raE1nSVlNV1g0TVE'}

names = {'BR':'Brute',
        'CH':'Cragheart',
        'MT':'Mindthief',
        'SC':'Scoundrel',
        'SW':'Spellweaver',
        'TI':'Tinkerer',
        'BT':'Beast Tyrant'}

code_names = {'BR':'Brute',
            'CH':'Cragheart',
            'MT':'Mindthief',
            'SC':'Scoundrel',
            'SW':'Spellweaver',
            'TI':'Tinkerer',
            'BT':'Two Minis'}

code_names_inv = {v: k for k, v in code_names.items()}

races = {'BR':'Inox',
        'CH':'Savaas',
        'MT':'Vermling',
        'SC':'Human',
        'SW':'Orchid',
        'TI':'Quatryl',
        'BT': 'Vermling'}

classes = code_names.values()

class App:
    def __init__(self, master):
        self.main = master
        self.main.title('Ability Cards')

        self.index = 0
        self.hand_limit = 0
        self.card_level = 1

        self.classmenu_config()

    def classmenu_config(self):
        self.classvar = tk.StringVar(self.main)
        self.classvar.set(names['BR'])
        
        tk.Label(self.main, text="Class").pack()

        self.control_frame = tk.Frame(self.main)
        self.control_frame.pack()

        self.prev = tk.Button(self.control_frame, text = 'Prev', command = lambda: self.prev_card())
        self.prev.pack(side = tk.LEFT)
        
        self.classmenu = tk.OptionMenu(self.control_frame, self.classvar, *classes, command = lambda _: self.update_class())
        self.classmenu.pack(side = tk.LEFT)

        self.next = tk.Button(self.control_frame, text = 'Next', command = lambda: self.next_card())
        self.next.pack(side = tk.LEFT)

        self.classname_label = tk.Label(self.main, text = 'Class Name')
        self.classname_label.pack()

        self.handlimit_label = tk.Label(self.main, text = 'Hand Limit: {}'.format(self.hand_limit))
        self.handlimit_label.pack()

        self.cardlevel_label = tk.Label(self.main, text = 'Card Level: {}'.format(self.card_level))
        self.cardlevel_label.pack()
        
        self.card_config()
        

    def card_config(self):
        self.get_class_cards()
        self.classname_label.config(text = '{} {}'.format(self.classrace, self.classname))
        self.handlimit_label.config(text = 'Hand Limit: {}'.format(self.hand_limit))
        self.get_card(self.index)
        
        self.cardimg = tk.Label(self.main, image=self.card)
        self.cardimg.pack()

    def update_class(self):
        self.get_class_cards()
        self.get_card(2*self.index)
        self.update_card()
        self.classname_label.config(text = '{} {}'.format(self.classrace, self.classname))
        self.handlimit_label.config(text = 'Hand Limit: {}'.format(self.hand_limit))

    def update_card(self):
        self.cardimg.config(image = self.card)
        self.cardlevel_label.config(text = 'Card Level: {}'.format(self.card_level))

    def next_card(self):
        if self.index < self.num_cards - 1:
            self.index += 1
        self.get_card(2*self.index)
        self.update_card()

    def prev_card(self):
        if self.index > 0:
            self.index -= 1
        self.get_card(2*self.index)
        self.update_card()

    def get_class_cards(self):
        self.ghclass = code_names_inv[self.classvar.get()]
        self.classname = names[self.ghclass]
        self.classrace = races[self.ghclass]

        fileid = resources[self.ghclass]
        fileurl = resourceurl + fileid

        response = urllib.request.urlopen(fileurl)
        data = response.read()

        
        self.cards = pdf2image.convert_from_bytes(data, fmt='ppm')
        self.num_cards = int(len(self.cards)/2)
        self.hand_limit = int(self.num_cards - 16 - 3)
        self.index = 0

    def get_card(self, index = 0):
        self.card = ImageTk.PhotoImage(self.cards[index])
        self.get_card_level()

    def get_card_level(self):
        if self.index < self.hand_limit:
            self.card_level = '1'
        elif self.index < self.hand_limit + 3:
            self.card_level = 'X'
        else:
            self.card_level = str(int((self.index - self.hand_limit - 3)/2)+2)
    

root = tk.Tk()
GUI = App(root)
root.mainloop()
root.destroy()
exit()