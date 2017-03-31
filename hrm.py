import bluepy.btle as btle
import hrmdelegate as dlgt

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
            self.hrm.setDelegate(dlgt.HRMMNotificationsDelegate())

            print "Ready to receive"

        except:
            print "Could not initialize"
            self.hrm.disconnect()


    def readHR(self):
        """
        Reads HR in an infinite loop
        """
        while(True):
            self.hrm.waitForNotifications(1.5)

    def readNPoints(self, n):
        """
        Reads N points of HR data (receives N notifications and finishes)
        """
        for i in range(n):
            self.hrm.waitForNotifications(1.5)

    def finish(self):
        self.hrm.disconnect()


if __name__ == '__main__':

    mac = "00:22:D0:85:88:8E"
    polar = HRMonitor(mac)
    polar.readNPoints(30)
    polar.finish()
