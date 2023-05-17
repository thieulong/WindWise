#!/usr/bin/python3
import functions
import pigpio
import time

import json

with open('/home/paul/WindWise/windmill_config.json') as file:
    windmill_config = json.load(file)

servo_pin = windmill_config['servo_pin']

max_angle = windmill_config['servo_max_angle']
min_angle = windmill_config['servo_min_angle']

default_angle = windmill_config['servo_default_angle']

pwm = pigpio.pi()
pwm.set_mode(servo_pin, pigpio.OUTPUT)

pwm.set_PWM_frequency( servo_pin, 50 )


def default_position():
    pwm.set_servo_pulsewidth( servo_pin, 1500) 

def shutdown():
    pwm.set_PWM_dutycycle(servo_pin, 0)
    pwm.set_PWM_frequency(servo_pin, 0)

def auto_change_angle(current_angle, new_angle):
    current_angle = int(current_angle)
    new_angle = int(new_angle)

    try:
        if new_angle > max_angle or new_angle < min_angle:
            return Exception
        
        else:
            if new_angle == current_angle:
                time.sleep(0.1)

            elif new_angle > current_angle:
                for angle in range(current_angle, new_angle):
                    angle = functions.map_range(angle, 0, 180, 500, 2500)
                    pwm.set_servo_pulsewidth(servo_pin, angle) 
                    time.sleep(0.1)

            elif new_angle < current_angle:
                for angle in range(current_angle, new_angle, -1):
                    angle = functions.map_range(angle, 0, 180, 500, 2500)
                    pwm.set_servo_pulsewidth(servo_pin, angle) 
                    time.sleep(0.1)
    except:
        shutdown()

def manual_change_angle(new_angle):
    new_angle = int(new_angle)

    try:
        if new_angle > max_angle or new_angle < min_angle:
            return Exception
        
        else:
            angle = functions.map_range(new_angle, 0, 180, 500, 2500)
            pwm.set_servo_pulsewidth(servo_pin, angle) 
            time.sleep(0.1)

    except:
        shutdown()
