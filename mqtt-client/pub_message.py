#!/usr/bin/python

import paho.mqtt.client as mqtt
import ssl
import sensor_module as sensor_mod
import time
import datetime

host="mosquitto-svr"
port=8883

#The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

def on_log(client, obj, level, string):
    print obj + level + string

def on_publish(client, userdata, mid):
	print("Published message")

temp_value=sensor_mod.getTemperature()
ts=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.on_publish = on_publish

client.tls_set(ca_certs="/home/pi/test-root-ca.crt", certfile="/home/pi/client.crt", keyfile="/home/pi/client.key",tls_version=ssl.PROTOCOL_TLSv1)
#print str(temp_value) + " " + str(ts)
msg_payload="[{\"temperature\":"+str(temp_value)+"},{\"timestamp\":\""+str(ts)+"\"}]"
print msg_payload
client.connect(host, port, 0)
client.publish("home/temperature", payload=msg_payload, qos=0, retain=False)
client.disconnect()

