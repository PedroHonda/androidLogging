import subprocess
import threading
import time

def loggingProcess(procName):
    ps=""
    while(len(ps)<2):
        ps = subprocess.getoutput("adb shell ps -A | grep " + procName).split()
    print(time.strftime("%Y-%m-%d %H:%M:%S") + " Process " + procName + " started!!! id=" + ps[1])
    while(1):
        ps = subprocess.getoutput("adb shell ps -A | grep " + procName).split()
        if len(ps)>1:
            print(time.strftime("%Y-%m-%d %H:%M:%S") + " Process " + procName + " running... id=" + ps[1])
        else:
            print(time.strftime("%Y-%m-%d %H:%M:%S") + " Process " + procName + " terminated...")
            return
        time.sleep(1)

def loggingFileSize(filePath):
    while(1):
        du = subprocess.getoutput("adb shell du " + filePath).split()[0]
        if "du" not in du:
            print(time.strftime("%Y-%m-%d %H:%M:%S") + " File " + filePath + " size=" + du)
        else:
            print(time.strftime("%Y-%m-%d %H:%M:%S") + " File " + filePath + " not found...")
            return
        time.sleep(1) 

tProcess = threading.Thread(target = lambda: loggingProcess("tcpdump"))
tProcess.start()
tFile = threading.Thread(target = lambda: loggingFileSize("/sdcard/Logging/packets.pcap"))
tFile.start()