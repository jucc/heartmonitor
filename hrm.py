import bluepy.btle as btle
import time
import numpy as np
import matplotlib.pyplot as plt


class HRMMNotificationsDelegate(btle.DefaultDelegate):
    """
     Delegate class will be set to handle hrmm notifications
     When notifications arrive, the HR value will be stored into bpm variable
    """
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        self.bpm = []

    def handleNotification(self, cHandle, data):
        self.bpm.append(ord(data[1]))


class HRMonitor:

    def __init__(self, mac):
        """
        Connects to the device via its mac address
        """
        hrm = 0

        try:
            self.hrm = btle.Peripheral(mac)
            print "Connected to device"
        except:
            print "Could not connect"
        self.configure()


    def configure(self):
        """
        Reads GATT specs and sets the handler for HR notifications
        Must be called upon initialization only
        """
        try:
            # read fixed ble specs for hrm service and hrmm characteristic
            hrmid = btle.AssignedNumbers.heart_rate
            hrmmid = btle.AssignedNumbers.heart_rate_measurement
            cccid = btle.AssignedNumbers.client_characteristic_configuration

            # query device for the service (hrm), characteristics and descriptors
            serv = self.hrm.getServiceByUUID(hrmid)
            chars = serv.getCharacteristics(hrmmid)[0]
            desc = self.hrm.getDescriptors(serv.hndStart, serv.hndEnd)
            d = [d for d in desc if d.uuid==cccid][0]

            # register handler to receive notifications
            self.hrm.writeCharacteristic(d.handle, '\1\0')
            self.hrm.setDelegate(HRMMNotificationsDelegate())
            self.t0 = time.time()

            print "Ready to receive"

        except:
            print "Could not initialize"
            self.hrm.disconnect()

    def readAndPrintHR(self):
        """
        Prints every notification received
        This is supposed to be called inside a loop
        """
        self.hrm.waitForNotifications(1.5)
        print "[%.2f]"%(time.time()-self.t0), self.hrm.delegate.bpm[-1]

    def finish(self):
        self.hrm.disconnect()


if __name__ == '__main__':

    mac = "00:22:D0:85:88:8E"
    polar = HRMonitor(mac)
    for i in range(30):
        polar.readAndPrintHR()
    polar.finish()
