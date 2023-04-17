#!/usr/bin/python3
def map_range(value, leftMin, leftMax, rightMin, rightMax):
    
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    valueScaled = float(value - leftMin) / float(leftSpan)

    return rightMin + (valueScaled * rightSpan)