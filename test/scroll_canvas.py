from tkinter import *
root=Tk()
frame=Frame(root,width=500,height=300)
frame.pack()
canvas=Canvas(frame,bg='#FFFFFF',width=500,height=300,scrollregion=(0,0,1500,300))
hbar=Scrollbar(frame,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview)
canvas.config(xscrollcommand=hbar.set)
inner_frame = Frame(canvas)
canvas.create_window(600, 100, window=inner_frame)
canvas.pack(side=LEFT, fill = BOTH, expand = TRUE)

frames = []
labels2 = []
labels = []
image = PhotoImage(file='C:\\Users\\InnSight\\Documents\\Github\\Gloomhaven-Deck-Builder\\icons\\summon.png')
for i in range(0,20):
    frames.append(Frame(inner_frame))
    frames[i].pack(side=LEFT)
    labels.append(Label(frames[i], image=image, relief=SUNKEN))
    labels[i].pack()
    labels2.append(Label(frames[i], text = 'Frame {}'.format(i)))
    labels2[i].pack()

root.mainloop()