#!/usr/bin/python3
import servo_control
import rotary_angle
import functions
import RPi.GPIO as GPIO
import paho.mqtt.client as paho
from paho import mqtt
import threading
import timer_multithreading
import time
import json

with open('/home/paul/WindWise/windmill_config.json') as file:
    windmill_config = json.load(file)

with open('/home/paul/WindWise/mqtt_config.json') as file:
    mqtt_config = json.load(file)

reset_duration = windmill_config['reset_duration']

GPIO.setwarnings(False)

current_angle = round(functions.map_range(rotary_angle.current_reading(), 0, 999, 0, 180))
servo_control.manual_change_angle(current_angle)

mqtt_username = mqtt_config['mqtt_username']
mqtt_password = mqtt_config['mqtt_password']
mqtt_cluster = mqtt_config['mqtt_cluster']

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

flag = 0

while True:
    wind_direction = rotary_angle.current_reading()
    new_angle = round(functions.map_range(wind_direction, 0, 999, 0, 180))
    if new_angle not in range(current_angle-5, current_angle+5):
        with open("angles.txt", 'w') as file:
            file.write("{}\n".format(current_angle))
            file.write("{}\n".format(new_angle))
        flag += 1
        print("Flag:",flag)
        if flag > 1:
            flag -= 1
            stop_event.set()
        stop_event = threading.Event()
        timer_thread = threading.Thread(target=timer_multithreading.start_timer, args=(stop_event,))
        timer_thread.start()
    servo_control.auto_change_angle(current_angle, new_angle)
    current_angle = new_angle
    client.publish("windmill/windmill_1/angle", payload=current_angle, qos=0)
    time.sleep(reset_duration)