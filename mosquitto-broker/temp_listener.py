#!/usr/bin/python

import paho.mqtt.client as mqtt
import db_module as db_module
import ssl
import time
import datetime
import json

#The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    json_data=str(msg.payload)
    data = json.loads(json_data)
    temp_data=data[0]["temperature"]
    ts_data=data[1]["timestamp"]
    print str(temp_data) + " " + str(ts_data)
    db_module.insertTempRecord(temp_data,ts_data)
	
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

def on_log(client, obj, level, string):
    print obj + level + string

def on_publish(client, userdata, mid):
	print("Published message")

tls_values={'ca_certs':"/etc/mosquitto/client_certs/test-root-ca.crt",'keyfile':"/etc/mosquitto/client_certs/client.key",'certfile':"/etc/mosquitto/client_certs/client.crt"}

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.on_publish = on_publish

client.tls_set(ca_certs="/etc/mosquitto/client_certs/test-root-ca.crt", certfile="/etc/mosquitto/client_certs/client.crt", keyfile="/etc/mosquitto/client_certs/client.key",tls_version=ssl.PROTOCOL_TLSv1)
client.connect("mosquitto-svr", 8883, 5)
client.subscribe("home/temperature");
client.loop_forever()
