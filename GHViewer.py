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
import cv2
import numpy as np


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
        self.top = [190, 80, 150, 160]
        self.btm = [190, 315, 150, 150]
        self.hough = [30, 13, 4, 1]

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
        #self.title_entry.pack(side = tk.RIGHT)
        self.initiative_frame = tk.Frame(self.stats_frame)
        self.initiative_frame.pack(anchor = tk.NW, fill = tk.X)
        self.initiative_label = tk.Label(self.initiative_frame, text = 'Initiative:')
        self.initiative_label.pack(side = tk.LEFT)
        self.initiative_entry = tk.Entry(self.initiative_frame)
        self.initiative_entry.bind('<Return>', lambda event: self.update_initiative())
        #self.initiative_entry.pack(side = tk.RIGHT)
        self.index_label = tk.Label(self.stats_frame, text = 'Index:')
        self.index_label.pack(anchor = tk.NW)
        self.edit_frame = tk.Frame(self.stats_frame)
        #self.edit_frame.pack(anchor = tk.NW, fill = tk.X)
        self.edit_card_button = tk.Button(self.edit_frame, text = 'Edit', command = lambda: self.edit_card())
        self.edit_card_button.pack(side = tk.LEFT)
        self.save_card_button = tk.Button(self.edit_frame, text = 'Save', command = lambda: self.save_card())
        self.save_card_button.pack(side = tk.LEFT)
        self.enchancement_label = tk.Label(self.stats_frame, text = 'Enhancements')
        self.enchancement_label.pack(anchor = tk.NW)
        self.enhancement_button = tk.Button(self.stats_frame, text = 'Show', command = lambda: self.find_enchancements())
        self.enhancement_button.pack(anchor = tk.NW)
        
        p1 = tk.IntVar(root)
        p1.set(self.hough[0])
        p1_label = tk.Label(self.stats_frame, text = 'P1')
        p1_label.pack(anchor = tk. NW)
        self.p1_spin = tk.Spinbox(self.stats_frame, from_ = 20, to = 40, textvariable = p1)
        self.p1_spin.pack(anchor = tk.NW)

        p2 = tk.IntVar(root)
        p2.set(self.hough[1])
        p2_label = tk.Label(self.stats_frame, text = 'p2')
        p2_label.pack(anchor = tk. NW)
        self.p2_spin = tk.Spinbox(self.stats_frame, from_ = 5, to = 25, textvariable = p2)
        self.p2_spin.pack(anchor = tk.NW)

        maxr = tk.IntVar(root)
        maxr.set(self.hough[2])
        maxr_label = tk.Label(self.stats_frame, text = 'maxr')
        maxr_label.pack(anchor = tk. NW)
        self.maxr_spin = tk.Spinbox(self.stats_frame, from_ = 0, to = 10, textvariable = maxr)
        self.maxr_spin.pack(anchor = tk.NW)

        minr = tk.IntVar(root)
        minr.set(self.hough[3])
        minr_label = tk.Label(self.stats_frame, text = 'minr')
        minr_label.pack(anchor = tk. NW)
        self.minr_spin = tk.Spinbox(self.stats_frame, from_ = 0, to = 10, textvariable = minr)
        self.minr_spin.pack(anchor = tk.NW)

        '''
        box = [256, 146, 300, 50]
        x = tk.IntVar(root)
        x.set(box[0])
        x_label = tk.Label(self.stats_frame, text = 'x')
        x_label.pack(anchor = tk. NW)
        self.x_spin = tk.Spinbox(self.stats_frame, from_ = 0, to = 500, textvariable = x)
        self.x_spin.pack(anchor = tk.NW)

        y = tk.IntVar(root)
        y.set(box[1])
        y_label = tk.Label(self.stats_frame, text = 'y')
        y_label.pack(anchor = tk. NW)
        self.y_spin = tk.Spinbox(self.stats_frame, from_ = 0, to = 500, textvariable = y)
        self.y_spin.pack(anchor = tk.NW)

        w = tk.IntVar(root)
        w.set(box[2])
        w_label = tk.Label(self.stats_frame, text = 'w')
        w_label.pack(anchor = tk. NW)
        self.w_spin = tk.Spinbox(self.stats_frame, from_ = 0, to = 500, textvariable = w)
        self.w_spin.pack(anchor = tk.NW)

        h = tk.IntVar(root)
        h.set(box[3])
        h_label = tk.Label(self.stats_frame, text = 'h')
        h_label.pack(anchor = tk. NW)
        self.h_spin = tk.Spinbox(self.stats_frame, from_ = 0, to = 500, textvariable = h)
        self.h_spin.pack(anchor = tk.NW)
        '''

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
        self.card_index = self.index + global_index[self.ghclass]
        try:
            with open('ghclass\{0}\data\{1:03d}.txt'.format(self.ghclass, self.card_index), 'r') as f:
                s = f.read()
                self.card_data = eval(s)
        except FileNotFoundError:
            pass

        self.cardimg.config(image = self.card)
        self.cardlevel_label.config(text = 'Card Level: {}'.format(self.card_data['level']))
        self.index_label.config(text = 'Index: {}'.format(self.card_index))
        self.title_label.config(text = 'Title: {}'.format(self.card_data['title']))
        self.initiative_label.config(text = 'Inititative: {}'.format(self.card_data['initiative']))

    def edit_card(self):
        self.card_data[self.card_index] = {'Title':'', 'Initiative':0, 'Enhancements':{}}

    def save_card(self):
        f = open('ghclass\{}\data\{}.txt'.format(self.ghclass, self.card_index),"w")
        f.write(str(self.card_data[self.ghclass]))
        f.close()

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
            
            #Extract image
            card = pdf2image.convert_from_bytes(self.data, dpi = self.dpi,
                                                      thread_count=self.thread_count,
                                                      first_page=ndx,
                                                      last_page=ndx,
                                                      fmt=self.fmt)
            #Add to list of cards for class
            self.cards.append(card[0])
            
            #Save the card image
            card_index = ndx//2 + global_index[self.ghclass]
            fpath = 'ghclass\{}\img'.format(self.ghclass)
            Path(fpath).mkdir(exist_ok=True,parents=True)
            card[0].save('{}\{}.{}'.format(fpath, card_index, self.fmt))

            #Update status bar when all class cards are loaded
            if len(self.cards) == self.num_cards:
                self.status_label.config(text = '{}: ready'.format(self.classname))

    def parse_cards(self):
        #data directory
        datapath = 'ghclass\{}\data'.format(self.ghclass)
        Path(datapath).mkdir(exist_ok=True,parents=True)

        #Get pdf
        pdfpath = 'ghclass\{}'.format(self.ghclass)
        pdffile = '{}\{} Cards.pdf'.format(pdfpath, self.ghclass)
        
        #Extract text
        raw = parser.from_file(pdffile)
        cards = raw['content'].split('{}\n'.format(names[self.ghclass]))
        for card in cards[1:-1]:
            #Identify summons
            pass

            #Parse card data
            data = list(filter(None, card.split('\n\n')))
            index = data[-1]
            level, title = data[-2].split('\n')
            initiative = data[-3].split(' ')[-1]
            output = {'index': index, 'title': title, 'level': level, 'initiative': initiative}

            #Save data
            with open('{}\{}.txt'.format(datapath, index),"w") as f:
                f.write(str(output))
    
    def find_enchancements(self):
        #resource locations
        imgpath = 'ghclass\{}\img'.format(self.ghclass)
        imgfile = '{}.{}'.format(self.card_index, self.fmt)

        #Load image
        data = cv2.imread('{}\{}'.format(imgpath, imgfile))
        gray_img = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(gray_img, 5)

        #Detection parameters
        #params = {'mdist': 10, 'p1': 30, 'p2': 14, 'minr': 0, 'maxr':4}
        params = {'mdist': 10, 
                'p1': int(self.p1_spin.get()), 
                'p2': int(self.p2_spin.get()), 
                'minr': int(self.minr_spin.get()), 
                'maxr': int(self.maxr_spin.get())}

        circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,
                                params['mdist'],
                                param1 = params['p1'],
                                param2 = params['p2'],
                                minRadius = params['minr'],
                                maxRadius=  params['maxr'])
        circles = np.uint16(np.around(circles))

        #Find enhancement locations
        x0 = -10
        w = 180
        h = 30
        self.enchancements = []
        for circ in circles[0,:]:
            #Dot parameters
            cx = circ[0]
            cy = circ[1]
            
            #Check Top/Btm Actions
            (xt,yt,wt,ht) = tuple(self.top)
            (xb,yb,wb,hb) = tuple(self.btm)
            if (xt < cx < xt+wt) and (yt < cy < yt+ht):
                self.enchancements.append({'location': (cx,cy), 'action': 'TOP', 'type': ''})
            elif (xb < cx < xb+wb) and (yb < cy < yb+hb):
                self.enchancements.append({'location': (cx,cy), 'action': 'BTM', 'type': ''})

        #Find AoEs
        _, threshold = cv2.threshold(gray_img, 240, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.hexes = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 900 < area < 1000:
                arc = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.03*arc, True)
                if len(approx) == 6:
                    cv2.drawContours(data, [approx], 0, (0, 255, 0), 2)
                    s = arc/6
                    h = 0.5*s*np.sqrt(3)
                    m = cv2.moments(approx)
                    cx = m['m10']/m['m00']
                    cy = m['m01']/m['m00']
                    self.hexes.append({'location': (cx, cy), 'length': s})

        #Mark the enhancement
        for e in self.enchancements:
            if len(self.hexes) > 0:
                for hex in self.hexes:
                    d = self.distance(e['location'], hex['location'])
                    if 35 < d < 37:
                        e['type'] = 'hex'
                        cv2.circle(data,e['location'],3,(255,0,0),2)
                        break
                else:
                    cv2.circle(data,e['location'],3,(0,255,0),2)
            else:
                cv2.circle(data,e['location'],3,(0,255,0),2)

        '''
        #Mark the enchancement
        #Box the adjacent text
        if not FP:
            cv2.circle(data,(cx,cy),r,color,2)
            x = cx - w + x0
            y = cy - h//2
            cv2.rectangle(data, (x, y), (x+w, y+h), color, 1)
        '''
        
        #Show Data
        cv2.imshow("Enhancements", data)

    def distance(self, p1: tuple, p2: tuple):
        sum = 0
        if len(p1) != len(p2):
            return None
        else:
            for (a, b) in zip(p1, p2):
                sum += (b - a)**2
        return np.sqrt(sum)

    def get_class_cards(self):
        #Class metadata
        self.ghclass = code_names_inv[self.classvar.get()]
        self.classname = names[self.ghclass]
        self.classrace = races[self.ghclass]
        self.hand_limit = hand_limits[self.ghclass]
        self.num_cards = self.hand_limit + 3 + 2*8
        self.index = 0

        #Class online card resources as pdf
        #Future: check for cached cards
        fileid = resources[self.ghclass]
        fileurl = resourceurl + fileid
        response = urllib.request.urlopen(fileurl)
        self.data = response.read()
        
        #Save the pdf resource
        pdfpath = 'ghclass\{}'.format(self.ghclass)
        Path(pdfpath).mkdir(exist_ok=True,parents=False)
        pdffile = '{}\{} Cards.pdf'.format(pdfpath, self.ghclass)
        urllib.request.urlretrieve(fileurl, pdffile)   
        
        #Parse card data
        self.parse_cards()

        #Parse card images from pdf in background thread
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
