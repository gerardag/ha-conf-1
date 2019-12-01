import paho.mqtt.publish as publish
import paho.mqtt.client as paho
from mitemp_bt.mitemp_bt_poller import MiTempBtPoller
from btlewrap.bluepy import BluepyBackend


def mqttPutMetric(mqttid, data):
    #publish.single(mqttid, payload=data, hostname="192.168.1.142", port=8883, auth={'username':'hassio','password':'aleixo'})
    client = paho.Client("mqtt-ble-sensor-com")
    client.username_pw_set('hassio', 'aleixo')
    client.connect('192.168.1.142', 8883)
    ret = client.publish(mqttid, payload=data, qos=0, retain=True)
    print("Added data '%s' to '%s'" % (data, mqttid))


def getXiaomiData(mac, device_name):
    print("Getting data from %s/%s..." % (mac, device_name))
    poller = MiTempBtPoller(mac, BluepyBackend)
    poller.fill_cache()
    temperature = poller.parameter_value('temperature',False)
    humidity = poller.parameter_value('humidity',False)
    print("Found data (%s/%s): Temperature=%s, Humidity=%s" %
          (mac, device_name, temperature, humidity))
    mqttPutMetric("ble/%s/humidity" % device_name, humidity)
    mqttPutMetric("ble/%s/temperature" % device_name, temperature)
    print("")


# Menjador
getXiaomiData("4c:65:a8:da:a0:e0", "menjador")

# Dormitori
getXiaomiData("4c:65:a8:da:a2:79", "dormitori")
