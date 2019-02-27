# Based on templates from: https://stackoverflow.com/questions/7546050 by Bryan Oakley
######################################################################################
import tkinter as tk
from tkinter import font  as tkfont
from tkinter import ttk

import subprocess
import adbCommands

class AndroidLoggingGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.centralize(550,550)
        
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("StartPage")

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



class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.updateADBdevices()

        # Label to Drop Down Menu for Android devices available
        dropMenuDevicesText = ttk.Label(self, text="Choose an Android device:")
        dropMenuDevicesText.grid(row=0, column=0, sticky="nsew")
        # Drop Menu containing all devices attached
        self.dropMenuDevicesSet = tk.StringVar()
        self.dropMenuDevicesSet.set(self.devices[0])
        self.dropMenuDevices = ttk.OptionMenu(self, self.dropMenuDevicesSet, self.devices[0], *self.devices, command=self.changeDevice)
        self.dropMenuDevices.grid(row=0, column=1, sticky="nsew")
        # Button to update current devices
        dropMenuDevicesUpdate = ttk.Button(self, text="UPDATE", command=self.updateADBdevices)
        dropMenuDevicesUpdate.grid(row=0, column=2, sticky="nsew")
        

    def updateADBdevices(self):
        self.devices = []
        self.android = ''
        adbDevices = subprocess.getoutput("adb devices")
        for d in adbDevices.split("\n"):
            if "\tdevice" in d:
                self.devices.append(d.split("\tdevice")[0])
        if not self.devices:
            self.devices.append("No Devices attached")
        else:
            self.android = self.devices[0]

    def changeDevice(self, value):
        if "No Devices attached" not in value:
            self.android = value

    def refreshDevices(self):
        self.updateADBdevices()
        menu = self.dropMenuDevices["menu"]
        menu.delete(0, "end")
        for d in self.devices:
            menu.add_command(label=d, command=lambda value=d: self.dropMenuDevicesSet.set(value))


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.showFrame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.showFrame("StartPage"))
        button.pack()