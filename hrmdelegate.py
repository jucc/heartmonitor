import bluepy.btle as btle
import time

class HRMMNotificationsDelegate(btle.DefaultDelegate):
    """
     Delegate class will be set to handle hrmm notifications
     In its first version, the handler will only print values to screen
    """
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        self.t0 = time.time()

    def handleNotification(self, cHandle, data):
        bpm = ord(data[1])
        print "[%.2f]"%(time.time()-self.t0), bpm
