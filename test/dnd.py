import tkinter as tk

# The factory function
def dnd_start(source, event):
    h = DndHandler(source, event)
    if h.root:
        return h
    else:
        return None

# The class that does the work
class DndHandler:
    root = None
    def __init__(self, source, event):
        if event.num > 5:
            return
        root = event.widget._root()
        try:
            root.__dnd
            return # Don't start recursive dnd
        except AttributeError:
            root.__dnd = self
            self.root = root
        self.source = source
        self.target = None
        self.initial_button = button = event.num
        self.initial_widget = widget = event.widget
        self.release_pattern = "<B%d-ButtonRelease-%d>" % (button, button)
        self.save_cursor = widget['cursor'] or ""
        widget.bind(self.release_pattern, self.on_release)
        widget.bind("<Motion>", self.on_motion)
        widget['cursor'] = "hand2"

    def __del__(self):
        root = self.root
        self.root = None
        if root:
            try:
                del root.__dnd
            except AttributeError:
                pass

    def on_motion(self, event):
        x, y = event.x_root, event.y_root
        target_widget = self.initial_widget.winfo_containing(x, y)
        source = self.source
        new_target = None
        while target_widget:
            try:
                attr = target_widget.dnd_accept
            except AttributeError:
                pass
            else:
                new_target = attr(source, event)
                if new_target:
                    break
            target_widget = target_widget.master
        old_target = self.target
        if old_target is new_target:
            if old_target:
                old_target.dnd_motion(source, event)
        else:
            if old_target:
                self.target = None
                old_target.dnd_leave(source, event)
            if new_target:
                new_target.dnd_enter(source, event)
                self.target = new_target

    def on_release(self, event):
        self.finish(event, 1)

    def cancel(self, event=None):
        self.finish(event, 0)

    def finish(self, event, commit=0):
        target = self.target
        source = self.source
        widget = self.initial_widget
        root = self.root
        try:
            del root.__dnd
            self.initial_widget.unbind(self.release_pattern)
            self.initial_widget.unbind("<Motion>")
            widget['cursor'] = self.save_cursor
            self.target = self.source = self.initial_widget = self.root = None
            if target:
                if commit:
                    target.dnd_commit(source, event)
                else:
                    target.dnd_leave(source, event)
        finally:
            source.dnd_end(target, event)


# ----------------------------------------------------------------------
# The rest is here for testing and demonstration purposes only!

class DnDLabel(tk.Label):
    def __init__(self, master, **kwargs):
        self.kwargs = {}
        self.kwargs.update(**kwargs)
        self.master = master
        self.canvas = self.label = self.id = None
        self.attach(self.master)

    def config(self, **kwargs):
        self.kwargs.update(**kwargs)
        if self.label is not None:
            self.label.config(**kwargs)
    
    def attach(self, master, x=0, y=0):
        canvas = master.canvas
        if canvas is self.canvas:
            self.canvas.coords(self.id, x, y)
            return
        if self.canvas:
            self.detach()
        if not canvas:
            return
        
        label = tk.Label(canvas, self.kwargs)
        id = canvas.create_window(x, y, window=label, anchor="nw")
        self.canvas = canvas
        self.label = label
        self.id = id
        self.label.bind("<ButtonPress>", self.press)

    def detach(self):
        canvas = self.canvas
        if not canvas:
            return
        id = self.id
        label = self.label
        self.canvas = self.label = self.id = None
        canvas.delete(id)
        label.destroy()

    def press(self, event):
        if dnd_start(self, event):
            # where the pointer is relative to the label widget:
            self.x_off = event.x
            self.y_off = event.y
            # where the widget is relative to the canvas:
            self.x_orig, self.y_orig = self.canvas.coords(self.id)

    def move(self, event):
        x, y = self.where(self.canvas, event)
        self.canvas.coords(self.id, x, y)

    def putback(self):
        self.canvas.coords(self.id, self.x_orig, self.y_orig)

    def where(self, canvas, event):
        # where the corner of the canvas is relative to the screen:
        x_org = canvas.winfo_rootx()
        y_org = canvas.winfo_rooty()
        # where the pointer is relative to the canvas widget:
        x = event.x_root - x_org
        y = event.y_root - y_org
        # compensate for initial pointer offset
        return x - self.x_off, y - self.y_off

    def dnd_end(self, target, event):
        pass


class DnDFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=1, fill = tk.BOTH)
        self.canvas.dnd_accept = self.dnd_accept
        self.snap = False

    def set_snap(self, snap: bool):
        self.snap = snap

    def dnd_accept(self, source, event):
        return self

    def dnd_enter(self, source, event):
        self.canvas.focus_set() # Show highlight border
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = source.canvas.bbox(source.id)
        dx, dy = x2-x1, y2-y1
        self.dndid = self.canvas.create_rectangle(x, y, x+dx, y+dy)
        self.dnd_motion(source, event)

    def dnd_motion(self, source, event):
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = self.canvas.bbox(self.dndid)
        self.canvas.move(self.dndid, x-x1, y-y1)

    def dnd_leave(self, source, event):
        self.master.focus_set() # Hide highlight border
        self.canvas.delete(self.dndid)
        self.dndid = None

    def dnd_commit(self, source, event):
        self.dnd_leave(source, event)
        if self.snap:
            (x, y) = (0, 0)
        else:
            x, y = source.where(self.canvas, event)
        source.attach(self, x, y)


def test():  
    root = tk.Tk()
    root.geometry("+1+1")
    left_frame = tk.Frame(root, bd = 5, bg = '#0000FF')
    left_frame.pack(side = tk.LEFT, anchor = tk.NW, expand = tk.TRUE, fill = tk.BOTH)
    right_frame = tk.Frame(root, bd = 5, bg = '#FF0000')
    right_frame.pack(side = tk.LEFT, anchor = tk.NW, expand = tk.TRUE, fill = tk.BOTH)
    
    left_dnd_frame = DnDFrame(left_frame)
    right_dnd_frame = DnDFrame(right_frame)
    left_dnd_frame.pack()
    right_dnd_frame.pack()
    left_dnd_frame.config(bd = 5, relief = tk.RAISED)
    right_dnd_frame.config(bd = 5, relief = tk.SUNKEN)
    
    image1 = tk.PhotoImage(file = 'shield.png')
    dnd_label1 = DnDLabel(left_dnd_frame, text='Label1', borderwidth=2, relief="raised", bg = 'red', image = image1)
    dnd_label2 = DnDLabel(right_dnd_frame, text='Label2', borderwidth=2, relief="raised", bg = 'blue')
    
    #dnd_label1.config(text='Left-Blue')
    #dnd_label2.config(text='Right-Red')
    
    root.mainloop()

if __name__ == '__main__':
    test()