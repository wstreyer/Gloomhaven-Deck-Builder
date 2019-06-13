import tkinter as tk
from PIL import Image, ImageTk
import os

class GHCLass():
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
    
    def __init__(self, ghclass):
        self.ghclass = ghclass
        self.hand_limit = GHCLass.hand_limits[self.ghclass]
        self.global_index = GHCLass.global_index[self.ghclass]
        self.class_name = GHCLass.names[self.ghclass]
        self.race = GHCLass.races[self.ghclass]
        self.code_name = GHCLass.code_names[self.ghclass]
        self.path = os.path.join(os.getcwd(), 'ghclass', ghclass)
        
class GHCharacter(GHClass):
    def __init__(self, ghclass: str, name: str, xp = 0, gold = 0):
        self.ghclass = ghclass
        super.__init__(self.ghclass)
        self.char_name = name
        self.level = 1
        self.xp = xp
        self.gold = gold
        self.active_card_pool = list(range(self.global_index, (self.global_index+13)))
        self.decks = []

    def add_deck(self, cards: list):
        self.decks.append(GHDeck())
        
class GHDeck(GHCharacter):
    def __init__(self, name, cards = []):
        self.deck_name = name
        self.cards = []
        self.add_cards(cards)
        
    def add_cards(self, cards: list):
        for card in cards:
            self.add_card(card)
    
    def add_card(self, card: int):
        self.cards.append(card)
        
    def rmv_cards(self, cards: list):
        for card in cards:
            self.rmv_card(card)
    
    def rmv_card(self, card: int):
        pass
        #self.cards.append(card)

class Card_Carousel(tk.Canvas):
    def __init__(self, master, imgpath, files = []):
        self.W = root.winfo_screenwidth()
        self.H = root.winfo_screenheight()
        self.imgpath = imgpath
        self.files = files
        self.images = []
        self.cards = []
        self.frames = []
        self.frame = tk.Frame(master, bd = 5, relief = tk.SUNKEN)
        self.frame.pack(fill = tk.X, expand = tk.TRUE)

        self.canvas = tk.Canvas(self.frame, bg = '#FFFFFF', scrollregion = (0, 0, int(2*self.W), int(self.H/2)))
        self.hbar = tk.Scrollbar(self.frame,orient = tk.HORIZONTAL)
        self.hbar.pack(side = tk.BOTTOM, fill = tk.X)
        self.hbar.config(command = self.canvas.xview)

        self.canvas.config(xscrollcommand = self.hbar.set)
        self.inner = tk.Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor = tk.NW, window = self.inner)
        self.canvas.pack(fill = tk.X, expand = tk.TRUE)

        cards = os.listdir(self.imgpath)
        cards = [int(card.split('.')[0]) for card in cards]
        self.class_index = min(cards)

        if len(self.files) > 0:
            cards = [card for card in cards if card in self.files]
        cards.sort()
        self.num_cards = len(cards)

        for i, card in enumerate(cards):
            img  = Image.open('{}\{}'.format(self.imgpath, '{}.png'.format(card)))
            (w, h) = img.size
            (w, h) = (int(w/2), int(h/2))
            img = img.resize((w, h), Image.ANTIALIAS)

            self.images.append(ImageTk.PhotoImage(img))

            W = (w + 10)*self.num_cards
            self.canvas.config(scrollregion=(0, 0, W, h))

            self.frames.append(tk.Frame(self.inner))
            self.frames[i].pack(side = tk.LEFT)

            self.cards.append(tk.Label(self.frames[i], image = self.images[i]))
            self.cards[i].pack()

root = tk.Tk()
pcwd = os.path.dirname(os.getcwd())
cardpath = '{}\\ghclass\\BR\\img'.format(pcwd)
character_frame = tk.Frame(root, bd = 5, relief = tk.SUNKEN)
character_frame.pack(side = tk.LEFT, fill = tk.Y, anchor = tk.NW, expand = tk.FALSE)
test_image = tk.PhotoImage(file = '{}\{}.png'.format(cardpath, 1))
test_label = tk.Label(character_frame, image = test_image)
test_label.pack(side = tk.LEFT, anchor = tk.NW)

card_frame = tk.Frame(root, bd = 5, relief = tk.SUNKEN)
card_frame.pack(side = tk.LEFT, fill = tk.X, expand = tk.TRUE, anchor = tk.NW)


active_card_pool = list(range(1,14))
deck1 = list(range(1,11))
deck2 = [1, 3, 4, 5, 6, 7, 8, 11, 12, 13]

ACP = Card_Carousel(card_frame, cardpath, files = active_card_pool)
Deck1 = Card_Carousel(card_frame, cardpath, files = deck1)

root.mainloop()
