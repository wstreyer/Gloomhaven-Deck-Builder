import tkinter as tk
from PIL import Image, ImageTk
import os








card_frames = []
titles = []
cards = []
images = []

class_index = 0
num_cards = 13


class Card_Carousel(tk.Canvas):
    def __init__(self, master, imgpath):
        self.W = root.winfo_screenwidth()
        self.H = root.winfo_screenheight()
        self.imgpath = imgpath
        self._

        self.canvas = tk.Canvas(master, bg = '#FFFFFF', scrollregion = (0, 0, int(2*self.W), int(self.H/2)))
        self.hbar = tk.Scrollbar(frame,orient = tk.HORIZONTAL)
        self.hbar.pack(side = tk.BOTTOM, fill = tk.X)
        self.hbar.config(command = self.canvas.xview)

        self.canvas.config(xscrollcommand = self.hbar.set)
        self.inner = tk.Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor = tk.NW, window = self.inner)
        self.canvas.pack(fill = tk.NONE, expand = tk.FALSE)

        for i in range(0, num_cards):    
            img  = Image.open('{}\{}'.format(cardpath, '{}.png'.format(class_index+1+i)))
            (w, h) = img.size
            (w, h) = (int(2*w/3), int(2*h/3))
            img = img.resize((w, h), Image.ANTIALIAS)

            images.append(ImageTk.PhotoImage(img))


            W = (w + 10)*num_cards
            canvas.config(scrollregion=(0, 0, W, 550))
            card_frames.append(tk.Frame(inner_frame))
            card_frames[i].pack(side = tk.LEFT)
            
            cards.append(tk.Label(card_frames[i], image = images[i]))
            cards[i].pack()
            
            titles.append(tk.Label(card_frames[i], text = 'Card {}'.format(class_index+1+i)))
            titles[i].pack()

root = tk.Tk()
frame = tk.Frame(root,width=1920,height=1080)

pcwd = os.path.dirname(os.getcwd())
cardpath = '{}\\ghclass\\BR\\img'.format(pcwd)
carousel = Card_Carousel(frame, cardpath)

frame.pack()
root.mainloop()