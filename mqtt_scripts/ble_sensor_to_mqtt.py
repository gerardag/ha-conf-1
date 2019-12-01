import paho.mqtt.publish as publish
import paho.mqtt.client as paho
from bluepy.btle import Scanner, DefaultDelegate, Peripheral

SCAN_TIME = 10.0

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)

    def handleNotification(ch,data):
        print("ch %s data %s" % (ch,data))


def mqttPutMetric(mqttid, data):
    #publish.single(mqttid, payload=data, hostname="192.168.1.142", port=8883, auth={'username':'hassio','password':'aleixo'})

    client = paho.Client("mqtt-ble-sensor-com")
    client.username_pw_set('hassio','aleixo')
    client.connect('192.168.1.142', 8883)
    ret = client.publish(mqttid,payload=data,qos=0,retain=True)
    print(ret)
    print("Added data '%s' to '%s'" % (data, mqttid))


# def processXiaomi(dev, device_name):
# #    per = Peripheral(dev.addr)
# #    per.withDelegate(ScanDelegate())
# #    for s in per.getServices():
# #        for c in s.getCharacteristics():
# #            print(c.read())
#     for (adtype, desc, value) in dev.getScanData():
#         print(" %s %s = %s" % (adtype, desc, value))
#         if (adtype == 22):
#             b = bytearray(value, 'utf-8')
#             print(b)
#             humidity = round(float(int(b[9:13],16)) / 1000,1)
#             temperature = round(((float(int(b[2:6],16)) / 1000) - 32) * 5/9,1)

#             print(float(int(b[2:6],16)))

#             mqttPutMetric("ble/%s/humidity" % device_name, humidity)
#             mqttPutMetric("ble/%s/temperature" % device_name, temperature)

#             print("temp %s hum %s" % (temperature, humidity))

def processBeewi(dev, device_name):
    for (adtype, desc, value) in dev.getScanData():
        print(" %s %s = %s" % (adtype, desc, value))
        if (adtype == 255):
            b = bytes.fromhex(value)
            temperature = int.from_bytes(b[4:6], "little")
            humidity = int(b[7])
            if (temperature >= 32768):
                temperature = temperature - 65535
            temperature = temperature / 10

            mqttPutMetric("ble/%s/humidity" % device_name, humidity)
            mqttPutMetric("ble/%s/temperature" % device_name, temperature)

            print("temp %s hum %s" % (temperature, humidity))

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(SCAN_TIME)

for dev in devices:
    device_name = None
    brand = None
    if (dev.addr == "d0:5f:b8:51:9b:36"):
        device_name = "exterior"
        brand = "beewi"
    # if (dev.addr == "4c:65:a8:da:a2:79"):
    #     device_name = "dormitori"
    #     brand = "xiaomi"
    # if (dev.addr == "4c:65:a8:da:a0:e0"):
    #     device_name = "menjador"
    #     brand = "xiaomi"

    if (device_name == None):
        continue

    print("Device is '%s'!" % device_name)

    # if (brand == "xiaomi"):
    #     processXiaomi(dev, device_name)
    if (brand == "beewi"):
        processBeewi(dev, device_name)
