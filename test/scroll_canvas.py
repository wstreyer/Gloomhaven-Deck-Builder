import tkinter as tk
from PIL import Image, ImageTk
import os
import ghclass
import dnd

class Card_Carousel(tk.Canvas):
    def __init__(self, master, imgpath, files: [int]):
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
        self.canvas.pack(fill = tk.X, expand = tk.FALSE)

        cards = os.listdir(self.imgpath)
        cards = [int(card.split('.')[0]) for card in cards]
        self.class_index = min(cards)
        self.hand_limit = len(cards)-3-16
        (w, h) = Image.open('{}\{}'.format(self.imgpath, '{}.png'.format(cards[0]))).size
        (w, h) = (int(w/2), int(h/2))

        if len(self.files) > 0:
            cards = [card for card in cards if card in self.files]
            cards.sort()    
            self.num_cards = len(cards)
        else:
            self.num_cards = self.hand_limit
            
        for i in range(0, self.num_cards):
            card = cards[i]
            img  = Image.open('{}\{}'.format(self.imgpath, '{}.png'.format(card)))
            img = img.resize((w, h), Image.ANTIALIAS)

            self.images.append(ImageTk.PhotoImage(img))

            W = (w + 10)*self.num_cards
            self.canvas.config(scrollregion=(0, 0, W, h))

            self.frames.append(dnd.DnDFrame(self.inner, width = w, height = h))
            self.frames[i].pack(side = tk.LEFT, fill = tk.NONE, expand = tk.FALSE)
            self.frames[i].set_snap(True)
            self.frames[i].pack_propagate(0)

            self.cards.append(dnd.DnDLabel(self.frames[i], image = self.images[i]))
            self.cards[i].label.pack(side=tk.LEFT)
            if len(self.files) == 0:
                self.cards[i].label.pack_forget()

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
#deck1 = list(range(1,11))
deck1 = []
deck2 = [1, 3, 4, 5, 6, 7, 8, 11, 12, 13]

ACP = Card_Carousel(card_frame, cardpath, files = active_card_pool)
Deck1 = Card_Carousel(card_frame, cardpath, files = deck1)
Table1 = dnd.DnDFrame(card_frame).pack(fill = tk.BOTH, expand = tk.FALSE)

root.mainloop()
