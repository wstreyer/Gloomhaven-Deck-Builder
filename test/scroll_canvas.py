from tkinter import *
import os


root=Tk()
frame=Frame(root,width=1920,height=1080)
frame.pack()
canvas=Canvas(frame,bg='#FFFFFF',width=1820,height=550,scrollregion=(0,0,11200,550))
hbar=Scrollbar(frame,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview)
canvas.config(xscrollcommand=hbar.set)
inner_frame = Frame(canvas)
canvas.create_window(0, 0, anchor = NW, window=inner_frame)
canvas.pack(side=LEFT, fill = NONE, expand = FALSE)


pcwd = os.path.dirname(os.getcwd())
cardpath = '{}\\ghclass\\BR\\img'.format(pcwd)
card_frames = []
titles = []
cards = []
images = []

class_index = 0
num_cards = 13
   
for i in range(0, num_cards):    
    images.append(PhotoImage(file = '{}\{}'.format(cardpath, '{}.png'.format(class_index+1+i))))
    w = (images[0].width() +10)*num_cards
    canvas.config(scrollregion=(0,0, w, 550))
    card_frames.append(Frame(inner_frame))
    card_frames[i].pack(side=LEFT)
    
    cards.append(Label(card_frames[i], image=images[i]))
    cards[i].pack()
    
    titles.append(Label(card_frames[i], text = 'Card {}'.format(class_index+1+i)))
    titles[i].pack()

root.mainloop()