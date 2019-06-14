import os

class GHClass():
    names = {'BR':'Brute',
        'CH':'Cragheart',
        'MT':'Mindthief',
        'SC':'Scoundrel',
        'SW':'Spellweaver',
        'TI':'Tinkerer',
        'BT':'Beast Tyrant',
        'BE':'Beserker',
        'QM':'Quartermaster',
        'NS':'Nightshroud',
        'DS':'Doomstalker',
        'SS':'-',
        'SK':'-',
        'EL':'Elementalist',
        'SU':'-',
        'PH':'-',
        'SB':'Sawbone',
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
            'EL':'Savaas',
            'SU':'-',
            'PH':'-',
            'SB':'Human',
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
        self.hand_limit = GHClass.hand_limits[self.ghclass]
        self.global_index = GHClass.global_index[self.ghclass]
        self.class_name = GHClass.names[self.ghclass]
        self.race = GHClass.races[self.ghclass]
        self.code_name = GHClass.code_names[self.ghclass]
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