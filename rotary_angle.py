#!/usr/bin/python3
import json
from grove_rotary_angle_sensor import GroveRotaryAngleSensor

with open('/home/paul/Automated-Windmill/windmill_config.json') as file:
    windmill_config = json.load(file)

rotary_pin = windmill_config['rotary_potentiometer_pin']

sensor = GroveRotaryAngleSensor(rotary_pin)

max_range = 999
min_range = 0

def current_reading():
    try:
        value = sensor.value
        if value < min_range or value > max_range:
            return Exception
        else:
            return value
    except:
        return
