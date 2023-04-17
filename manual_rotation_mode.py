#!/usr/bin/python3
import servo_control
import RPi.GPIO as GPIO
import sys
import time


GPIO.setwarnings(False)

new_angle = int(sys.argv[1])

servo_control.manual_change_angle(new_angle)

time.sleep(0.1)


