import bluepy.btle as btle
import time

polarmac = "00:22:D0:85:88:8E"

# handler function definition
def hrmmNotificationHandler(cHandle, data):
    bpm = ord(data[1])
    print "[%.2f]"%(time.time()-t0), bpm

# MAIN

hrm = 0
try:
    #connect to device
    hrm = btle.Peripheral(polarmac)
    print "connected"

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
    hrm.delegate.handleNotification = hrmmNotificationHandler

    # START GOING

    t0 = time.time()
    while(True):
        hrm.waitForNotifications(1.5)

finally:
    hrm.disconnect()
