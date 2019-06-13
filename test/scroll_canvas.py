import tkinter as tk
from PIL import Image, ImageTk
import os

class Card_Carousel(tk.Canvas):
    def __init__(self, master, imgpath):
        self.W = root.winfo_screenwidth()
        self.H = root.winfo_screenheight()
        self.imgpath = imgpath
        self.images = []
        self.cards = []
        self.frames = []
        self.frame = tk.Frame(master)
        self.frame.pack(fill = tk.X, expand = tk.TRUE)

        self.canvas = tk.Canvas(self.frame, bg = '#FFFFFF', scrollregion = (0, 0, int(2*self.W), int(self.H/2)))
        self.hbar = tk.Scrollbar(self.frame,orient = tk.HORIZONTAL)
        self.hbar.pack(side = tk.BOTTOM, fill = tk.X)
        self.hbar.config(command = self.canvas.xview)

        self.canvas.config(xscrollcommand = self.hbar.set)
        self.inner = tk.Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor = tk.NW, window = self.inner)
        self.canvas.pack(fill = tk.BOTH, expand = tk.TRUE)

        cards = os.listdir(self.imgpath)
        cards = [int(card.split('.')[0]) for card in cards]
        self.class_index = min(cards)
        self.num_cards = len(cards)

        for i in range(0, self.num_cards):    
            img  = Image.open('{}\{}'.format(self.imgpath, '{}.png'.format(self.class_index+i)))
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
frame = tk.Frame(root,width=1920,height=1080)
frame.pack()
frame.pack_propagate(0)
pcwd = os.path.dirname(os.getcwd())
cardpath = '{}\\ghclass\\BR\\img'.format(pcwd)
carousel1 = Card_Carousel(frame, cardpath)
carousel2 = Card_Carousel(frame, cardpath)
root.mainloop()