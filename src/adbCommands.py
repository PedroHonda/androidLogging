import subprocess

class adbClass():
    def __init__(self, serialno):
        self.serialno = serialno
        subprocess.call("adb -s " + self.serialno + " shell mkdir /sdcard/Logging")
    
    def adbRoot(self):
        subprocess.call("adb -s " + self.serialno + " root")

    def cleanLogging(self):
        subprocess.call("adb -s " + self.serialno + " shell rm -rf /sdcard/Logging/*")

    def startVideo(self):
        """ 
            adb shell screenrecord /sdcard/Logging/video.mp4
        """
        subprocess.call("adb -s " + self.serialno + " shell screenrecord /sdcard/Logging/video.mp4")

    def stopVideo(self):
        """ 
            adb shell ps -A | grep screenrecord
            -- This gives some information about the process such as its PID, which can be used to kill the process with:
            -- adb shell kill -2 <PID>
        """
        psVideo = subprocess.getoutput("adb -s " + self.serialno + " shell ps -A | grep screenrecord").split()[1]
        if psVideo:
            subprocess.call("adb -s " + self.serialno + " shell kill -2 " + psVideo)
            return True
        else:
            return False
        
    def startAPlog(self):
        """ 
            adb shell "logcat > /sdcard/Logging/APlogging.txt"
        """
        subprocess.call("adb -s " + self.serialno + " shell \"logcat -b all > /sdcard/Logging/APlogging.txt\"")

    def stopAPlog(self):
        """ 
            adb shell ps -A | grep logcat
            -- This gives some information about the process such as its PID, which can be used to kill the process with:
            -- adb shell kill -2 <PID>
        """
        psLogcat = subprocess.getoutput("adb -s " + self.serialno + " shell ps -A | grep logcat").split()[1]
        if psLogcat:
            subprocess.call("adb -s " + self.serialno + " shell kill -2 " + psLogcat)
            return True
        else:
            return False

    def startTCPdump(self):
        """ 
            adb shell tcpdump -v -s 0 -i any -w /sdcard/Logging/packets.pcap
        """
        subprocess.call("adb -s " + self.serialno + " shell tcpdump -v -s 0 -i any -w /sdcard/Logging/packets.pcap")

    def stopTCPdump(self):
        """ 
            adb shell ps -A | grep tcpdump
            -- This gives some information about the process such as its PID, which can be used to kill the process with:
            -- adb shell kill -2 <PID>
        """
        psTCP = subprocess.getoutput("adb -s " + self.serialno + " shell ps -A | grep tcpdump").split()[1]
        if psTCP:
            subprocess.call("adb -s " + self.serialno + " shell kill -2 " + psTCP)
            return True
        else:
            return False