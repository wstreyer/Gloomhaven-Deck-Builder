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
import os
import pickle

#GH Class data
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

#Calculate distance between two points
def distance(p1: tuple, p2: tuple):
        sum = 0
        if len(p1) != len(p2):
            return None
        else:
            for (a, b) in zip(p1, p2):
                sum += (b - a)**2
        return np.sqrt(sum)

class App:
    def __init__(self, master):
        self.main = master
        self.main.title('Gloomhaven Deck Builder')

        #Global constants
        self.index = 0
        self.startup_class = 'BR'
        self.hand_limit = 0
        self.dpi = 150
        self.thread_count = 16
        self.fmt = 'png'
        self.card_data = {'level': 1}

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
        self.viewer.bind('<s>', lambda event: self.find_enhancements())
        self.viewer.bind('<f>', lambda event: self.find_enhancements())
        self.viewer.focus_set()

        #Stats frame
        self.stats_frame = tk.Frame(self.viewer)
        self.stats_frame.pack(side = tk.LEFT, anchor = tk.NW)

        #Card stats
        self.classname_label = tk.Label(self.stats_frame, text = 'Class:')
        self.classname_label.pack(anchor = tk.NW)
        self.handlimit_label = tk.Label(self.stats_frame, text = 'Hand Limit: {}'.format(self.hand_limit))
        self.handlimit_label.pack(anchor = tk.NW)
        self.cardlevel_label = tk.Label(self.stats_frame, text = 'Card Level: {}'.format(self.card_data['level']))
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
        self.enhancement_label = tk.Label(self.stats_frame, text = 'Enhancements')
        self.enhancement_label.pack(anchor = tk.NW)
        self.enhancement_frame = tk.Frame(self.stats_frame)
        self.enhancement_frame.pack(anchor = tk.NW)
        self.show_enhancement_button = tk.Button(self.enhancement_frame, text = 'Show', command = lambda: self.find_enhancements())
        self.show_enhancement_button.pack(side = tk.LEFT, anchor = tk.NW)
        self.find_enhancement_button = tk.Button(self.enhancement_frame, text = 'Find', command = lambda: self.find_enhancements())
        self.find_enhancement_button.pack(side = tk.LEFT, anchor = tk.NW)
        
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
            with open('ghclass\{0}\data\{1:03d}.dat'.format(self.ghclass, self.card_index), 'rb') as f:
                self.card_data = pickle.load(f)
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
        #pickled file
        with open('ghclass\{}\data\{}.dat'.format(self.ghclass, self.card_index),"wb") as f: 
            pickle.dump(self.card_data[self.ghclass], f)
        
        #readable text file
        with open('ghclass\{}\data\{}.txt'.format(self.ghclass, self.card_index),"w") as f: 
            f.write(str(self.card_data[self.ghclass]))

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

    def extract_cards(self, data=None, pdffile=''):
        #Parse pdf to get list of image objects
        #pdf contains card fronts and backs. Backs are skipped to same time.
        self.cards = []
        self.new_cards_needed = False
        for ndx in range(1, 2*self.num_cards +1, 2):
            if len(self.cards) > 0:
                self.status_label.config(text = '{}: loading card {}/{}'.format(self.classname, ndx//2 + 1, self.num_cards))
            
            #Extract image
            if data:
                card = pdf2image.convert_from_bytes(data, dpi = self.dpi,
                                                    thread_count=self.thread_count,
                                                    first_page=ndx,
                                                    last_page=ndx,
                                                    fmt=self.fmt)
            elif pdffile:
                card = pdf2image.convert_from_bytes(pdffile, dpi = self.dpi,
                                                    thread_count=self.thread_count,
                                                    first_page=ndx,
                                                    last_page=ndx,
                                                    fmt=self.fmt)
            else:
                raise ValueError
                return
            
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
        for card in cards[0:-1]:
            #Identify summons
            pass

            #Parse card data
            data = list(filter(None, card.split('\n\n')))
            index = data[-1]
            level, title = data[-2].split('\n')
            initiative = data[-3].split(' ')[-1]
            output = {'index': index, 'title': title, 'level': level, 'initiative': initiative, 'content': card[1:-4]}

            #Save data
            #pickle
            with open('{}\{}.dat'.format(datapath, index),"wb") as f:
                pickle.dump(output, f)
            
            #readable text file
            with open('{}\{}.txt'.format(datapath, index),"w") as f:
                f.write(str(output))
    
    def find_enhancements(self):
        #resource locations
        imgpath = 'ghclass\{}\img'.format(self.ghclass)
        imgfile = '{}.{}'.format(self.card_index, self.fmt)

        #Load image
        self.card_rgb = cv2.imread('{}\{}'.format(imgpath, imgfile))
        img_gray = cv2.cvtColor(self.card_rgb, cv2.COLOR_BGR2GRAY)
        
        #Find ability icons
        icons = self.find_icons()
        
        #Check if card has a summon and which action it is (top or btm)
        summon = 'none'
        for i in icons:
            if i['type'] == 'summon': 
                print('Summon on {} action'.format(i['action']))
                summon = i['action']
                break
        self.card_data['summon'] = summon

        #Find possible enhancment locations
        enhancements = self.find_circles(img_gray, summon = summon)

        #Find AoE hexes
        hexes = self.find_hexagon(img_gray)
        
        #Find all top and btm hexes
        hex1 = [hex for hex in hexes if (hex['action'] == 'top')]
        hex2 = [hex for hex in hexes if (hex['action'] == 'btm')]
        
        #Determine if top AoE is melee or not
        for hex in hex1:
            if 'melee' in hex:
                melee = True
                break
        else:
            melee = False
        self.card_data['hex1'] = len(hex1) - int(melee)
        
        #Determine if btm AoE is melee or not
        for hex in hex2:
            if 'melee' in hex:
                melee = True
                break
        else:
            melee = False
        self.card_data['hex2'] = len(hex2) - int(melee)
        
        #Find attack hex enhancements
        for e in enhancements:
            if len(hexes) > 0:
                for hex in hexes:
                    d = distance(e['xy'], hex['xy'])
                    if 34 < d < 40:
                        e['type'] = 'hex'
                        cv2.circle(self.card_rgb,e['xy'],3,(255,0,0),2)
                        break
                else:
                    e['type'] = 'ability'
                    #cv2.circle(self.card_rgb,e['xy'],3,(0,255,0),2)
            else:
                e['type'] = 'ability'
                #cv2.circle(self.card_rgb,e['xy'],3,(0,255,0),2)

        #Match icons with ability enhancements
        for e in enhancements:
            if e['type'] == 'ability':
                for i in icons:
                    dx = e['xy'][0] - i['xy'][0]
                    dy = e['xy'][1] - i['xy'][1]
                    #print('({}, {})'.format(dx, dy))
                    
                    xmax = 60 if i['action'] == summon else 90
                    if 37 <= dx <= xmax and 0 < dy <= 17:
                        if i['type'] == 'heal' and i['action'] == summon:
                            e['type'] = 'health' if i['action'] == summon else i['type']
                        else:
                            e['type'] = i['type']
                        print(e)
                        cv2.circle(self.card_rgb,e['xy'],3,(0,255,0),2)
                        x = i['xy'][0]
                        y = i['xy'][1]
                        w = i['size'][0]
                        h = i['size'][1]
                        cv2.rectangle(self.card_rgb, (x,y), (x+w, y+h), (0,255,0), 2)
                        break
                else:
                    e['type'] = 'remove'
                    print(e)
            else:
                print(e)

        #Show Data
        cv2.imshow('Enhancements', self.card_rgb)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        #Remove false enhancements
        enhancements = [e for e in enhancements if not (e['type'] == 'remove')]
        self.card_data['enhancements'] = enhancements
        
        #Save data
        #data directory
        datapath = 'ghclass\{}\data'.format(self.ghclass)
        Path(datapath).mkdir(exist_ok=True,parents=True)

        #pickle        
        with open('{0}\{1:03d}.dat'.format(datapath, self.card_index),"wb") as f:
            pickle.dump(self.card_data, f)

        #readable text file
        with open('{0}\{1:03d}.txt'.format(datapath, self.card_index),"w") as f:
            f.write(str(self.card_data))

    def get_class_cards(self):
        #Class metadata
        self.ghclass = code_names_inv[self.classvar.get()]
        self.classname = names[self.ghclass]
        self.classrace = races[self.ghclass]
        self.hand_limit = hand_limits[self.ghclass]
        self.num_cards = self.hand_limit + 3 + 2*8
        self.index = 0

         #resource locations
        imgpath = 'ghclass\{}\img'.format(self.ghclass)
        datapath = ''
        pdffile = 'ghclass\{0}\{0} Cards.pdf'.format(self.ghclass)

        #Retrieve class card images
        if Path(imgpath).exists():
            self.cards = []
            for i in range(0, self.num_cards):
                imgfile = '{}.{}'.format(global_index[self.ghclass]+i, self.fmt)
                img = Image.open('{}\{}'.format(imgpath, imgfile))
                self.cards.append(img)
        else:
            if os.path.exists(pdffile):
                #load pdf data from file
                self.extract_thread = threading.Thread(target = self.extract_cards(pdffile=pdffile))
            else:
                #load pdf data from url
                #Class online card resources as pdf
                fileid = resources[self.ghclass]
                fileurl = resourceurl + fileid
                response = urllib.request.urlopen(fileurl)
                data = response.read()
                self.extract_thread = threading.Thread(target = self.extract_cards(data = data))
                
                #Save the pdf resource
                pdfpath = 'ghclass\{}'.format(self.ghclass)
                Path(pdfpath).mkdir(exist_ok=True,parents=False)
                urllib.request.urlretrieve(fileurl, pdffile)
            
            #Parse card images from pdf in background thread
            self.extract_thread.start()

        #Retrieve class card data
        try:
            raise NotImplementedError
            #open data directory
            
            pass
        except:
            #Parse card data
            self.parse_cards()

    def get_card(self, index = 0):
        while len(self.cards) <= index:
            time.sleep(0.250)
        
        self.card = ImageTk.PhotoImage(self.cards[index])

    def find_circles(self, data, summon = 'none', params = (30, 12, 1, 4), mdist = 10):
        #gray_img = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(data, 5)

        #Find circles for possible enhancement locations
        (p1, p2, minr, maxr) = params
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,1,
                                    mdist,
                                    param1 = p1,
                                    param2 = p2,
                                    minRadius = minr,
                                    maxRadius = maxr)
        circles = np.uint16(np.around(circles))

        #Set action bounding boxes
        if summon == 'top':
            (xt,yt,wt,ht) = (35, 75, 300, 165)
            (xb,yb,wb,hb) = (180, 310, 150, 155)
        elif summon == 'btm':
            (xt,yt,wt,ht) = (180, 75, 150, 165)
            (xb,yb,wb,hb) = (35, 310, 300, 155)
        else:
            (xt,yt,wt,ht) = (180, 75, 150, 165)
            (xb,yb,wb,hb) = (180, 310, 150, 155)
        
        #Show bounding box
        cv2.rectangle(self.card_rgb, (xt,yt), (xt+wt, yt+ht), (0,255,255), 2)
        cv2.rectangle(self.card_rgb, (xb,yb), (xb+wb, yb+hb), (0,255,255), 2)
        
        #Filter enhancement locations
        enhancements = []
        for circ in circles[0,:]:
            #Dot parameters
            cx = circ[0]
            cy = circ[1]
            
            #Check Top/Btm Actions
            if (xt < cx < xt+wt) and (yt < cy < yt+ht):
                #cv2.circle(self.card_rgb,(cx,cy),3,(0,255,0),2)
                enhancements.append({'xy': (cx,cy), 'action': 'top', 'type':''})
            elif (xb < cx < xb+wb) and (yb < cy < yb+hb):
                #cv2.circle(self.card_rgb,(cx,cy),3,(0,255,0),2)
                enhancements.append({'xy': (cx,cy), 'action': 'btm', 'type':''})
            else:
                pass

        return enhancements

    #Find Hexagons
    def find_hexagon(self, data):
        #gray_img = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(data, 240, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        hexes = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 900 < area < 1000:
                arc = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.03*arc, True)
                if len(approx) == 6:
                    cv2.drawContours(self.card_rgb, [approx], 0, (0, 255, 0), 2)
                    s = arc/6
                    h = 0.5*s*np.sqrt(3)
                    m = cv2.moments(approx)
                    cx = m['m10']/m['m00']
                    cy = m['m01']/m['m00']
                    action = 'top' if cy <= 262 else 'btm'
                    r = self.card_rgb[int(cy), int(cx), 2]
                    if r < 100: #AoE is melee
                        hexes.append({'xy': (cx, cy), 'length': s, 'action': action, 'melee': True})
                    else:
                        hexes.append({'xy': (cx, cy), 'length': s, 'action': action})
        return hexes

    #look for all known icons
    def find_icons(self):
        # Convert it to grayscale 
        img_gray = cv2.cvtColor(self.card_rgb, cv2.COLOR_BGR2GRAY) 

        # Specify a threshold 
        thresholds = [{'icons': ['attack', 'move', 'heal', 'shield', 'retaliate'], 'threshold': 0.89},
                    {'icons': ['range', 'invisible', 'wound', 'immobilize'], 'threshold': 0.72},
                    {'icons': ['summon', 'target', 'push', 'pull'], 'threshold': 0.86},
                    {'icons': ['pierce', 'poison'], 'threshold': 0.89}]

        pcwd = os.path.dirname(os.getcwd())
        iconpath = 'icons'.format()

        icons = []
        for icon in os.listdir(iconpath):   
            name = icon.split('.')[0]
            name = name.split('-')[0]
            
            #Choose threshold from thresholds
            for t in thresholds:
                if name in t['icons']:
                    threshold = t['threshold']
                    break      
            
            # Read the template icon
            template = cv2.imread(os.path.join(iconpath, icon),0)
            w, h = template.shape[::-1]
            
            # Perform match operations. 
            
            res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
            
            # Find the best match above threshold 
            best = cv2.minMaxLoc(res)
            if best[1] >= threshold:
                x = best[3][0]
                y = best[3][1]
                #print('{}: {} - {} - BEST'.format(name, best[1], (x,y)))
                action = 'top' if y <= 262 else 'btm'
                icons.append({'xy': (x,y), 'size': (w,h), 'type': name, 'action': action, 'match': best[1]})
                print(icons[-1])
                cv2.rectangle(self.card_rgb, (x,y), (x+w, y+h), (0,255,255), 2)
            
            # Find all other matches above threshold
            loc = np.where( res >= threshold)  
            prev = (0,0)
            for pt in zip(*loc[::-1]):
                x = pt[0]
                y = pt[1]
                if distance(best[3], (x,y)) > 10 and distance(prev, (x,y)) > 10:
                    #print('{}: {} - {}'.format(name, res[(y,x)], (x,y)))
                    action = 'top' if y <= 262 else 'btm'
                    icons.append({'xy': (x,y), 'size': (w,h), 'type': name, 'action': action, 'match': res[(y,x)]})
                    print(icons[-1])
                    cv2.rectangle(self.card_rgb, (x,y), (x+w, y+h), (0,255,255), 2)
                prev = (x,y)        
        return icons

root = tk.Tk()
GUI = App(root)
root.mainloop()
root.destroy()
exit()
