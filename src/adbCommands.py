import subprocess

class adbClass():
    def __init__(self, serialno):
        self.serialno = serialno
        subprocess.call("adb -s " + self.serialno + " shell mkdir /sdcard/Logging")
    
    def adbRoot(self):
        subprocess.call("adb -s " + self.serialno + " root")

    def startVideo(self):
        subprocess.call("adb -s " + self.serialno + " shell screenrecord /sdcard/Logging/video.mp4")
    
    def startAPlog(self):
        subprocess.call("adb -s " + self.serialno + " shell aplogcat -d -o /sdcard/Logging/ -n 1")

    def startTCPdump(self):
        subprocess.call("adb -s " + self.serialno + " shell tcpdump -v -s 0 -i any -w /sdcard/Logging/packets.pcap")

