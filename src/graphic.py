# Based on templates from: https://stackoverflow.com/questions/7546050 by Bryan Oakley
######################################################################################
import sys
if sys.version_info[0] == 3:
    import tkinter as tk                
    from tkinter import messagebox as tkMessageBox
    from tkinter import font  as tkfont 
    from tkinter import ttk             
    from tkinter import filedialog
else:
    import Tkinter as tk     
    import tkFont as tkfont  
    import ttk
    import tkFileDialog as filedialog
    import tkMessageBox

import subprocess
import adbCommands
import threading
import time

class AndroidLoggingGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.centralize(500,180)
        
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

        #self.config(bg="#91D5F9")

        # Integer to help on development
        currentRow = 0

        for i in range(0,8):
            self.columnconfigure(i, weight=1)
        
        # Label to Drop Down Menu for Android devices available
        tk.Label(self, text="Choose an Android device:", anchor="e").grid(row=currentRow, column=0, columnspan=3, sticky="nsew")
        # Drop Menu containing all devices attached
        self.dropMenuDevicesSet = tk.StringVar()
        self.dropMenuDevicesSet.set(self.devices[0])
        self.dropMenuDevices = tk.OptionMenu(self, self.dropMenuDevicesSet, self.devices[0], command=self.updateADBclass)
        self.dropMenuDevices.grid(row=currentRow, column=3, columnspan=3, sticky="nsew")
        # Button to update current devices
        dropMenuDevicesUpdate = ttk.Button(self, text="UPDATE", command=self.refreshDevices)
        dropMenuDevicesUpdate.grid(row=currentRow, column=6, columnspan=2, sticky="nsew")

        currentRow += 1
        rooting = tk.Button(self, text="Rooting", bg="#000000", fg="#FFFFFF", command=self.adbRooting)
        rooting.grid(row=currentRow, column=0, columnspan=8, sticky="nsew")

        currentRow += 1
        tk.Label(self, text="Video capture:", anchor="e").grid(row=currentRow, column=1, sticky="nswe")
        self.collectVideoVar = tk.IntVar()
        self.collectVideo = tk.Checkbutton(self, variable=self.collectVideoVar)
        self.collectVideo.grid(row=currentRow, column=2)

        currentRow += 1
        tk.Label(self, text="AP log:", anchor="e").grid(row=currentRow, column=1, sticky="nswe")
        self.collectAPVar = tk.IntVar()
        self.collectAP = tk.Checkbutton(self, variable=self.collectAPVar)
        self.collectAP.grid(row=currentRow, column=2)

        currentRow += 1
        tk.Label(self, text="TCP log:", anchor="e").grid(row=currentRow, column=1, sticky="nswe")
        self.collectTCPVar = tk.IntVar()
        self.collectTCP = tk.Checkbutton(self, variable=self.collectTCPVar)
        self.collectTCP.grid(row=currentRow, column=2)

        currentRow += 1
        separator2 = ttk.Separator(self, orient='horizontal')
        separator2.grid(row=currentRow, column=0, columnspan=8, sticky="nswe")

        currentRow += 1
        cleanLogs = tk.Button(self, text="CLEAN", bg="#0022BB", fg="#FFFFFF", command=self.cleanLogs, width=5)
        cleanLogs.grid(row=currentRow, column=0, sticky="nsew", columnspan=2)
        self.collectLogs = tk.Button(self, text="START", bg="#0022BB", fg="#FFFFFF", command=self.startLogCollection, width=5)
        self.collectLogs.grid(row=currentRow, column=2, sticky="nsew", columnspan=2)
        self.stopLogs = tk.Button(self, text="STOP", bg="#0022BB", fg="#FFFFFF", command=self.stopLogCollection, state="disabled", width=5)
        self.stopLogs.grid(row=currentRow, column=4, sticky="nsew", columnspan=2)
        pull = tk.Button(self, text="PULL", bg="#0022BB", fg="#FFFFFF", command=self.pullLogs, width=5)
        pull.grid(row=currentRow, column=6, sticky="nsew", columnspan=2)

        # added resizing configs
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)


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
            self.adb = adbCommands.adbClass(self.android)

    def refreshDevices(self):
        self.updateADBdevices()
        menu = self.dropMenuDevices["menu"]
        menu.delete(0, "end")
        for d in self.devices:
            menu.add_command(label=d, command=lambda value=d: self.dropMenuDevicesSet.set(value))

    def updateADBclass(self):
        self.adb = adbCommands.adbClass(self.android)
        
    def adbRooting(self):
        self.adb.adbRoot()

    def cleanLogs(self):
        self.adb.cleanLogging()

    def pullLogs(self):
        subprocess.call("adb pull /sdcard/Logging/ ./logs/" + str(time.strftime("%Y%m%d%H%M%S") + "/"))

    def startLogCollection(self):
        if self.collectVideoVar.get():
            tVideo = threading.Thread(target = self.adb.startVideo)
            tVideo.start()
        if self.collectAPVar.get():
            tAP = threading.Thread(target = self.adb.startAPlog)
            tAP.start()
        if self.collectTCPVar.get():
            tTCP = threading.Thread(target = self.adb.startTCPdump)
            tTCP.start()
        self.collectVideo.config(state="disabled")
        self.collectAP.config(state="disabled")
        self.collectTCP.config(state="disabled")
        self.collectLogs.config(state="disabled")
        self.stopLogs.config(state="active")
        
    def stopLogCollection(self):
        if self.collectVideoVar.get():
            tVideo = threading.Thread(target = self.adb.stopVideo)
            tVideo.start()
        if self.collectAPVar.get():
            tAP = threading.Thread(target = self.adb.stopAPlog)
            tAP.start()
        if self.collectTCPVar.get():
            tTCP = threading.Thread(target = self.adb.stopTCPdump)
            tTCP.start()
        self.collectVideo.config(state="active")
        self.collectAP.config(state="active")
        self.collectTCP.config(state="active")
        self.collectLogs.config(state="active")
        self.stopLogs.config(state="disabled")

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