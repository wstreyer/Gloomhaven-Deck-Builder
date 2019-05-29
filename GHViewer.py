# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:41:31 2019

@author: wstreyer
"""

from pathlib import Path
import urllib.request
import pdf2image
import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import threading
import time
from tika import parser


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

races = {'BR':'Inox',
        'CH':'Savaas',
        'MT':'Vermling',
        'SC':'Human',
        'SW':'Orchid',
        'TI':'Quatryl',
        'BT': 'Vermling'}

global_index = {'BR':1,
                'CH':145,
                'MT':116,
                'SC':88,
                'SW':61,
                'TI':30,
                'BT':447}

hand_limits = {'BR':10,
                'CH':11,
                'MT':10,
                'SC':9,
                'SW':8,
                'TI':12,
                'BT':10}

code_names = {'BR':'Brute',
            'CH':'Cragheart',
            'MT':'Mindthief',
            'SC':'Scoundrel',
            'SW':'Spellweaver',
            'TI':'Tinkerer',
            'BT':'Two Minis'}

code_names_inv = {v: k for k, v in code_names.items()}

classes = code_names.values()

class App:
    def __init__(self, master):
        self.main = master
        self.main.title('Gloomhaven Deck Builder')

        #Global constants
        self.index = 0
        self.startup_class = 'BR'
        self.hand_limit = 0
        self.card_level = 1
        self.dpi = 150
        self.thread_count = 16
        self.fmt = 'png'
        self.card_data = {}

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

        #Stats frame
        self.stats_frame = tk.Frame(self.viewer)
        self.stats_frame.pack(side = tk.LEFT, anchor = tk.NW)

        #Card stats
        self.classname_label = tk.Label(self.stats_frame, text = 'Class:')
        self.classname_label.pack(anchor = tk.NW)
        self.handlimit_label = tk.Label(self.stats_frame, text = 'Hand Limit: {}'.format(self.hand_limit))
        self.handlimit_label.pack(anchor = tk.NW)
        self.cardlevel_label = tk.Label(self.stats_frame, text = 'Card Level: {}'.format(self.card_level))
        self.cardlevel_label.pack(anchor = tk.NW)
        self.title_frame = tk.Frame(self.stats_frame)
        self.title_frame.pack(anchor = tk.NW, fill = tk.X)
        self.title_label = tk.Label(self.title_frame, text = 'Title:')
        self.title_label.pack(side = tk.LEFT)
        self.title_entry = tk.Entry(self.title_frame)
        self.title_entry.bind('<Return>', lambda event: self.update_title())
        self.title_entry.pack(side = tk.RIGHT)
        self.initiative_frame = tk.Frame(self.stats_frame)
        self.initiative_frame.pack(anchor = tk.NW, fill = tk.X)
        self.initiative_label = tk.Label(self.initiative_frame, text = 'Initiative:')
        self.initiative_label.pack(side = tk.LEFT)
        self.initiative_entry = tk.Entry(self.initiative_frame)
        self.initiative_entry.bind('<Return>', lambda event: self.update_initiative())
        self.initiative_entry.pack(side = tk.RIGHT)
        self.index_label = tk.Label(self.stats_frame, text = 'Index:')
        self.index_label.pack(anchor = tk.NW)
        self.edit_frame = tk.Frame(self.stats_frame)
        self.edit_frame.pack(anchor = tk.NW, fill = tk.X)
        self.edit_card_button = tk.Button(self.edit_frame, text = 'Edit', command = lambda: self.edit_card())
        self.edit_card_button.pack(side = tk.LEFT)
        self.save_card_button = tk.Button(self.edit_frame, text = 'Save', command = lambda: self.save_card())
        self.save_card_button.pack(side = tk.LEFT)

        #Viewer Frame
        self.viewer_frame = tk.Frame(self.viewer)
        self.viewer_frame.pack(side = tk.LEFT)

        #Viewer controls
        self.control_frame = tk.Frame(self.viewer_frame)
        self.control_frame.pack()
        self.prev = tk.Button(self.control_frame, text = 'Prev', command = lambda: self.prev_card())
        self.prev.pack(side = tk.LEFT)
        self.classvar = tk.StringVar(self.main)
        self.classvar.set(names[self.startup_class])
        self.classmenu = tk.OptionMenu(self.control_frame, self.classvar, *classes, command = lambda _: self.update_class())
        self.classmenu.pack(side = tk.LEFT)
        self.next = tk.Button(self.control_frame, text = 'Next', command = lambda: self.next_card())
        self.next.pack(side = tk.LEFT)       
        
        #Place to show card
        self.cardimg = tk.Label(self.viewer_frame)
        self.cardimg.pack()
        
        #Create status bar
        self.status_frame = tk.Frame(self.main)
        self.status_frame.pack(side = tk.BOTTOM, fill = tk.X)
        self.status_label = tk.Label(self.status_frame, text = '{}: '.format(names[self.startup_class]))
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

    def update_class(self):
        self.get_class_cards()
        self.get_card(2*self.index)
        self.update_card()
        self.classname_label.config(text = '{} {}'.format(self.classrace, self.classname))
        self.handlimit_label.config(text = 'Hand Limit: {}'.format(self.hand_limit))

    def update_card(self):
        self.cardimg.config(image = self.card)
        self.cardlevel_label.config(text = 'Card Level: {}'.format(self.card_level))
        self.card_index = self.index + global_index[self.ghclass]
        self.index_label.config(text = 'Index: {}'.format(self.card_index))

    def edit_card(self):
        self.card_data[self.card_index] = {'Title':'', 'Initiative':0, 'Enhancements':{}}

    def save_card(self):
        f = open('ghclass\{}\cards.txt'.format(self.ghclass),"w")
        f.write(str(self.card_data[self.ghclass]))
        f.close()
        print(self.card_data)

    def update_title(self):
        title = self.title_entry.get()
        self.card_data[self.card_index]['Title'] = title
        print(title)

    def update_initiative(self):
        initiative = self.initiative_entry.get()
        self.card_data[self.card_index]['Initiative'] = initiative
        print(initiative)

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

    def extract_cards(self):
        #Parse pdf to get list of image objects
        #pdf contains card fronts and backs. Backs are skipped to same time.
        self.cards = []
        self.new_cards_needed = False
        for ndx in range(1, 2*self.num_cards +1, 2):
            if len(self.cards) > 0:
                self.status_label.config(text = '{}: loading card {}/{}'.format(self.classname, ndx//2 + 1, self.num_cards))
            card = pdf2image.convert_from_bytes(self.data, dpi = self.dpi,
                                                      thread_count=self.thread_count,
                                                      first_page=ndx,
                                                      last_page=ndx,
                                                      fmt=self.fmt)
            self.cards.append(card[0])
            if len(self.cards) == self.num_cards:
                self.status_label.config(text = '{}: ready'.format(self.classname))
    
        #Cache cards locally
        self.export_cards()

    def parse_cards(self):
        #raw = parser.from_file(_)
        #parse the contents of raw['content'] into a dictionary
        pass

    def export_cards(self):
        for ndx, card in enumerate(self.cards):
            card_index = ndx + global_index[self.ghclass]
            fpath = 'ghclass\{}\img'.format(self.ghclass)
            Path(fpath).mkdir(exist_ok=True,parents=False)
            card.save('{}\{}.{}'.format(fpath, card_index, self.fmt))
    
    def parse_enchancements(self):
        pass

    def get_class_cards(self):
        #Class metadata
        self.ghclass = code_names_inv[self.classvar.get()]
        self.classname = names[self.ghclass]
        self.classrace = races[self.ghclass]
        self.hand_limit = hand_limits[self.ghclass]
        self.num_cards = self.hand_limit + 3 + 2*8
        self.index = 0
        try:
            with open('ghclass\{}\cards.txt'.format(self.ghclass), 'r') as f:
                s = f.read()
                self.card_data = eval(s)
                print(self.card_data)
        except FileNotFoundError:
            pass

        #Class online card resources as pdf
        #Future: check for cached cards
        fileid = resources[self.ghclass]
        fileurl = resourceurl + fileid
        response = urllib.request.urlopen(fileurl)
        self.data = response.read()
        
        #Parse cards from pdf in background thread
        self.extract_thread = threading.Thread(target = self.extract_cards)
        self.extract_thread.start()

    def get_card(self, index = 0):
        while len(self.cards) <= index:
            time.sleep(0.250)
        
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
