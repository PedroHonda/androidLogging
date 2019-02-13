import tkinter as tk

class AndroidLoggingGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.centralize(550,550)
        
        self.frames = {}

    def centralize(self, width, height):
        self.resizable(width=True, height=True)
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (width/2)
        y = (hs/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def showFrame(self, n):
        frame = self.frames[n]
        frame.update()
        frame.tkraise()


class someFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller