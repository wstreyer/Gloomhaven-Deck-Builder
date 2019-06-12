# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:41:31 2019

@author: wstreyer
"""

from pathlib import Path
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
from PIL import ImageTk, Image
import os
import pickle

#GH Class data
locked = {'BR':False,
        'CH':False,
        'MT':False,
        'SC':False,
        'SW':False,
        'TI':False,
        'BT':False,
        'BE':True,
        'QM':True,
        'NS':True,
        'DS':True,
        'SS':True,
        'SK':True,
        'EL':True,
        'SU':True,
        'PH':True,
        'SB':True,
        'DI':False}

resourceurl = 'https://drive.google.com/uc?export=download&id='

resources = {'BR':'0B8ppELln5Z0rdjJzSGZMYXNqVkE',
             'CH':'0B8ppELln5Z0raUNvY3BNbG1adjQ',
             'MT':'0B8ppELln5Z0rdFBmMFdkTXhLZ1U',
             'SC':'0B8ppELln5Z0rbTlRLUIxVk5NQlE',
             'SW':'0B8ppELln5Z0rYjhYQkV4bUpoOFE',
             'TI':'0B8ppELln5Z0rUVJRRGw1MTV5cTQ',
             'BT':'0B8ppELln5Z0raE1nSVlNV1g0TVE',
             'BE':'-',
             'QM':'-',
             'NS':'-',
             'DS':'-',
             'SS':'-',
             'SK':'-',
             'EL':'-',
             'SU':'-',
             'PH':'-',
             'SB':'-',
             'DI':'-'}

names = {'BR':'Brute',
        'CH':'Cragheart',
        'MT':'Mindthief',
        'SC':'Scoundrel',
        'SW':'Spellweaver',
        'TI':'Tinkerer',
        'BT':'Beast Tyrant',
        'BE':'-',
        'QM':'-',
        'NS':'-',
        'DS':'-',
        'SS':'-',
        'SK':'-',
        'EL':'-',
        'SU':'-',
        'PH':'-',
        'SB':'-',
        'DI':'Diviner'}

races = {'BR':'Inox',
        'CH':'Savaas',
        'MT':'Vermling',
        'SC':'Human',
        'SW':'Orchid',
        'TI':'Quatryl',
        'BT': 'Vermling',
        'BE':'-',
        'QM':'-',
        'NS':'-',
        'DS':'-',
        'SS':'-',
        'SK':'-',
        'EL':'-',
        'SU':'-',
        'PH':'-',
        'SB':'-',
        'DI':'Aesther'}

global_index = {'BR':1,
                'CH':145,
                'MT':116,
                'SC':88,
                'SW':61,
                'TI':30,
                'BT':447,
                'BE':319,
                'QM':205,
                'NS':261,
                'DS':376,
                'SS':348,
                'SK':175,
                'EL':476,
                'SU':233,
                'PH':289,
                'SB':407,
                'DI':574}

hand_limits = {'BR':10,
                'CH':11,
                'MT':10,
                'SC':9,
                'SW':8,
                'TI':12,
                'BT':10,
                'BE':10,
                'QM':9,
                'NS':9,
                'DS':12,
                'SS':9,
                'SK':11,
                'EL':10,
                'SU':9,
                'PH':11,
                'SB':21,
                'DI':9}

code_names = {'BR':'Brute',
            'CH':'Cragheart',
            'MT':'Mindthief',
            'SC':'Scoundrel',
            'SW':'Spellweaver',
            'TI':'Tinkerer',
            'BT':'Two Minis',
            'BE':'Lightning Bolts',
            'QM':'Three Spears',
            'NS':'Eclipse',
            'DS':'Grumpy Face',
            'SS':'Music Note',
            'SK':'Sun',
            'EL':'Triforce',
            'SU':'Circles',
            'PH':'Cthulu Face',
            'SB':'Saw',
            'DI':'Diviner'}

code_names_inv = {v: k for k, v in code_names.items()}

classes = code_names.values()

class App:
    def __init__(self, master):
        self.main = master
        self.main.title('Gloomhaven Deck Builder')

        #Global constants
        self.index = 0
        self.ghclass = 'BR'
        self.hand_limit = 0
        self.dpi = 150
        self.thread_count = 16
        self.fmt = 'png'
        self.card_data = {'level': 1}
        self.pcwd = os.path.dirname(os.getcwd())

        #Create a notebook
        self.nb = ttk.Notebook(self.main)
        self.nb.pack(fill = tk.BOTH, expand=tk.YES)
        
        #Configure each page of the notebook
        self.viewer_config()
        #self.characters_config()
        #self.decks_config()

    #Create the card viewer
    def viewer_config(self):
        #Add viewer as new notebook page
        self.viewer = tk.Frame(self.nb)
        self.nb.add(self.viewer, text = 'Viewer')
        self.viewer.bind('<Left>', lambda event: self.prev_card())
        self.viewer.bind('<Right>', lambda event: self.next_card())
        self.viewer.focus_set()

        #Stats frame
        self.stats_frame = tk.Frame(self.viewer, width = 160, height = 400)
        self.stats_frame.pack_propagate(0)
        self.stats_frame.pack(side = tk.LEFT, anchor = tk.NW)

        #Card stats
        self.classname_label = tk.Label(self.stats_frame, text = 'Class:', font = ('Pirata One', 12))
        self.classname_label.pack(anchor = tk.NW)
        self.handlimit_label = tk.Label(self.stats_frame, text = 'Hand Limit: {}'.format(self.hand_limit), font = ('Pirata One', 12))
        self.handlimit_label.pack(anchor = tk.NW)
        self.cardlevel_label = tk.Label(self.stats_frame, text = 'Card Level: {}'.format(self.card_data['level']), font = ('Pirata One', 12))
        self.cardlevel_label.pack(anchor = tk.NW)
        self.title_frame = tk.Frame(self.stats_frame)
        self.title_frame.pack(anchor = tk.NW, fill = tk.X)
        self.title_label = tk.Label(self.title_frame, text = 'Title:', font = ('Pirata One', 12))
        self.title_label.pack(side = tk.LEFT)
        self.initiative_frame = tk.Frame(self.stats_frame)
        self.initiative_frame.pack(anchor = tk.NW, fill = tk.X)
        self.initiative_label = tk.Label(self.initiative_frame, text = 'Initiative:', font = ('Pirata One', 12))
        self.initiative_label.pack(side = tk.LEFT)
        self.index_label = tk.Label(self.stats_frame, text = 'Index:', font = ('Pirata One', 12))
        self.index_label.pack(anchor = tk.NW)
        
        #Viewer Frame
        self.viewer_frame = tk.Frame(self.viewer)
        self.viewer_frame.pack(side = tk.LEFT)

        #Viewer controls
        self.control_frame = tk.Frame(self.viewer_frame)
        self.control_frame.pack()
        self.left_arrow = tk.PhotoImage(file = os.path.join(self.pcwd, 'assets', 'Icon Pack', 'widgets', 'left-arrow.png'))
        self.prev = tk.Button(self.control_frame, text = 'Prev', image = self.left_arrow, command = lambda: self.prev_card())
        self.prev.pack(side = tk.LEFT)
        self.classmenu = tk.Menubutton(self.control_frame, text="Class", font = ('Nyala', 10, 'bold'),relief=tk.RAISED )
        self.classmenu.menu = tk.Menu(self.classmenu, tearoff = 0 )
        self.classmenu["menu"] = self.classmenu.menu
        self.classmenu.pack(side = tk.LEFT)
        iconpath = os.path.join(self.pcwd, 'assets', 'Icon Pack', 'small')
        self.icons = {}
        for icon in os.listdir(iconpath):
            name = icon.split('-')[1]
            imgfile = os.path.join(self.pcwd, icon)
            self.icons[name] = tk.PhotoImage(file = imgfile)
            self.classmenu.menu.add_command(label='', image=self.icons[name], compound="left", command = lambda my_icon = name: self.update_class(my_icon))
        self.right_arrow = tk.PhotoImage(file = os.path.join(self.pcwd, 'assets', 'Icon Pack', 'widgets', 'right-arrow.png'))
        self.next = tk.Button(self.control_frame, text = 'Next', image = self.right_arrow, command = lambda: self.next_card())
        self.next.pack(side = tk.LEFT)       
        
        #Place to show card
        self.cardimg = tk.Label(self.viewer_frame)
        self.cardimg.pack()
        
        #Create status bar
        self.status_frame = tk.Frame(self.main)
        self.status_frame.pack(side = tk.BOTTOM, fill = tk.X)
        self.status_label = tk.Label(self.status_frame, text = '{}: '.format(names[self.ghclass]))
        self.status_label.pack(side = tk .LEFT)
        
        #Get cards
        self.card_config()

    def card_config(self):
        self.get_class_cards()
        self.classname_label.config(text = '{} {}'.format(self.classrace, self.classname))
        self.handlimit_label.config(text = 'Hand Limit: {}'.format(self.hand_limit))
        self.get_card(self.index)
        self.card_index = self.index + global_index[self.ghclass]
        self.index_label.config(text = 'Index: {}'.format(self.card_index))
        self.cardimg.config(image = self.card)

    def update_class(self, ghclass = ''):
        if ghclass == '':
            pass
        elif locked[ghclass]:
                mb.showinfo('', 'This class is locked')
                return
        else:
            self.ghclass = ghclass
        self.get_class_cards()
        self.get_card(self.index)
        self.update_card()
        self.classname_label.config(text = '{} {}'.format(self.classrace, self.classname))
        self.handlimit_label.config(text = 'Hand Limit: {}'.format(self.hand_limit))

    def update_card(self):
        self.card_index = self.index + global_index[self.ghclass]
        try:
            with open(os.path.join(self.pcwd, 'ghclass', self.ghclass, 'data', '{1:03d}.dat'.format(self.card_index)), 'rb') as f:
                self.card_data = pickle.load(f)
        except FileNotFoundError:
            pass

        self.cardimg.config(image = self.card)
        self.cardlevel_label.config(text = 'Card Level: {}'.format(self.card_data['level']))
        self.index_label.config(text = 'Index: {}'.format(self.card_index))
        self.title_label.config(text = 'Title: {}'.format(self.card_data['title']))
        self.initiative_label.config(text = 'Inititative: {}'.format(self.card_data['initiative']))

    def next_card(self):
        if self.index < self.num_cards - 1:
            self.index += 1
            self.get_card(self.index)
            self.update_card()

    def prev_card(self):
        if self.index > 0:
            self.index -= 1
            self.get_card(self.index)
            self.update_card()

    def get_class_cards(self):
        #Class metadata
        self.classname = names[self.ghclass]
        self.classrace = races[self.ghclass]
        self.hand_limit = hand_limits[self.ghclass]
        self.num_cards = self.hand_limit + 3 + 2*8
        self.index = 0

         #resource locations
        
        imgpath = os.path.join(self.pcwd, 'ghclass', self.ghclass, 'img')

        #Retrieve class card images
        if Path(imgpath).exists():
            self.cards = []
            for i in range(0, self.num_cards):
                imgfile = '{}.{}'.format(global_index[self.ghclass]+i, self.fmt)
                img = Image.open(os.path.join(imgpath, imgfile))    
                self.cards.append(img)
        
    def get_card(self, index = 0):
        self.card = ImageTk.PhotoImage(self.cards[index])
    
root = tk.Tk()
GUI = App(root)
root.mainloop()
root.destroy()
exit()
