import bluepy.btle as btle
from datetime import datetime
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


def hrm(mac):
    try:
        hrm = btle.Peripheral(mac)
        print "Connected to device"

        # read fixed ble specs for hrm service and hrmm characteristic
        hrmid = btle.AssignedNumbers.heart_rate
        hrmmid = btle.AssignedNumbers.heart_rate_measurement
        cccid = btle.AssignedNumbers.client_characteristic_configuration

        # query device for the service (hrm), characteristics and descriptors
        serv = hrm.getServiceByUUID(hrmid)
        chars = serv.getCharacteristics(hrmmid)[0]
        desc = hrm.getDescriptors(serv.hndStart, serv.hndEnd)
        d = [d for d in desc if d.uuid==cccid][0]

        # register handler to receive notifications
        hrm.writeCharacteristic(d.handle, '\1\0')
        hrm.setDelegate(HRMMNotificationsDelegate())

        # START GOING
        while(True):
            hrm.waitForNotifications(1.5)

    finally:
        hrm.disconnect()


if __name__ == '__main__':

    polarmac = "00:22:D0:85:88:8E"
    hrm(polarmac)
