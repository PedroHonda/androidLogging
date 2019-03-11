# Based on templates from: https://stackoverflow.com/questions/7546050 by Bryan Oakley
######################################################################################
import tkinter as tk
from tkinter import font  as tkfont
from tkinter import ttk

import subprocess
import adbCommands
import threading

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
        self.dropMenuDevices = tk.OptionMenu(self, self.dropMenuDevicesSet, self.devices[0], command=self.updateADBclass)
        self.dropMenuDevices.grid(row=0, column=1, sticky="nsew")
        # Button to update current devices
        dropMenuDevicesUpdate = ttk.Button(self, text="UPDATE", command=self.refreshDevices)
        dropMenuDevicesUpdate.grid(row=0, column=2, sticky="nsew")
        
        startVideo = tk.Button(self, text="Rooting", bg="#000000", fg="#FFFFFF", command=self.adbRooting)
        startVideo.grid(row=1, column=0, columnspan=3, sticky="nsew")

        startVideo = tk.Button(self, text="Start Video", bg="PaleGreen1", command=self.startingVideo)
        startVideo.grid(row=2, column=0, sticky="nsew")
        stopVideo = tk.Button(self, text="Stop Video", bg="#BB0000", command=self.stoppingVideo)
        stopVideo.grid(row=2, column=1, sticky="nsew")

        startAP = tk.Button(self, text="Start AP", bg="PaleGreen1", command=self.startingAP)
        startAP.grid(row=3, column=0, sticky="nsew")
        stopAP = tk.Button(self, text="Stop AP", bg="#BB0000", command=self.stoppingAP)
        stopAP.grid(row=3, column=1, sticky="nsew")

        startTCP = tk.Button(self, text="Start TCP", bg="PaleGreen1", command=self.startingTCP)
        startTCP.grid(row=4, column=0, sticky="nsew")
        stopTCP = tk.Button(self, text="Stop TCP", bg="#BB0000", command=self.stoppingTCP)
        stopTCP.grid(row=4, column=1, sticky="nsew")

        separator2 = ttk.Separator(self, orient='horizontal')
        separator2.grid(row=5, column=0, columnspan=3, sticky="nswe")

        cleanLogs = tk.Button(self, text="Cleaning Logs", bg="#0022BB", fg="#FFFFFF", command=self.cleanLogs)
        cleanLogs.grid(row=6, column=0, columnspan=2, sticky="nsew")

        pull = tk.Button(self, text="Pull Logs", bg="#0022BB", fg="#FFFFFF", command=self.pullLogs)
        pull.grid(row=7, column=0, columnspan=2, sticky="nsew")


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

    def startingVideo(self):
        t = threading.Thread(target = self.adb.startVideo)
        t.start()
    def stoppingVideo(self):
        self.adb.stopVideo()

    def startingAP(self):
        t = threading.Thread(target = self.adb.startAPlog)
        t.start()
    def stoppingAP(self):
        self.adb.stopAPlog()

    def startingTCP(self):
        t = threading.Thread(target = self.adb.startTCPdump)
        t.start()
    def stoppingTCP(self):
        self.adb.stopTCPdump()

    def cleanLogs(self):
        self.adb.cleanLogging()

    def pullLogs(self):
        subprocess.call("adb pull /sdcard/Logging/")
        

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