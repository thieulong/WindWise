import serial
import json
import paho.mqtt.client as paho
from paho import mqtt
import time
import random

with open('/home/paul/WindWise/windmill_config.json') as file:
    windmill_config = json.load(file)

windmill_name = windmill_config['name']

with open('/home/paul/WindWise/mqtt_config.json') as file:
    mqtt_config = json.load(file)

mqtt_username = mqtt_config['mqtt_username']
mqtt_password = mqtt_config['mqtt_password']
mqtt_cluster = mqtt_config['mqtt_cluster']

broker = mqtt_config['mqtt_broker']
port = int(mqtt_config['mqtt_port'])
topic = "windmill/windmill_1/current"
client_id = f'raspberrypi-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    emqx_client = paho.Client(client_id)
    emqx_client.on_connect = on_connect
    emqx_client.connect(broker, port)
    return emqx_client


def publish(emqx_client):
    if ser.in_waiting > 0:
        current = float(ser.readline().decode('utf-8').rstrip())
        msg = f"{current}"
        emqx_client.publish(topic, msg)

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_cluster, 8883)

client.on_message = on_message
client.on_publish = on_publish

emqx_client = connect_mqtt()
client.loop_start()

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

try:
    while True:
        if ser.in_waiting > 0:
            current = float(ser.readline().decode('utf-8').rstrip())
            print(current)
            if current < -37 or current > 37:
                error_msg = "{} - Motor current sensor failed".format(windmill_name)
                client.publish("windmill/windmill_1/status", payload=error_msg, qos=0)
            else:
                client.publish("windmill/windmill_1/current", payload=current, qos=0)
                time.sleep(1)
                publish(emqx_client)

except IOError:
    error_msg = "{} - Motor current sensor disconnected".format(windmill_name)
    client.publish("windmill/windmill_1/status", payload=error_msg, qos=0)
    time.sleep(1)
