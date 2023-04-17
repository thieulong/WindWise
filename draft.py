import smbus
import math
import time

# Set the I2C address of the module
ADDRESS = 0x0E

# Create an instance of the I2C bus
bus = smbus.SMBus(1)

# Write configuration data to the module
bus.write_byte_data(ADDRESS, 0x00, 0x70)
bus.write_byte_data(ADDRESS, 0x01, 0xA0)
bus.write_byte_data(ADDRESS, 0x02, 0x00)

# Function to read 16-bit data from the module
def read_data(address):
    high = bus.read_byte_data(ADDRESS, address)
    low = bus.read_byte_data(ADDRESS, address + 1)
    value = (high << 8) + low
    if (value >= 0x8000):
        return -((65535 - value) + 1)
    else:
        return value

# Function to calculate the direction
def get_direction(x, y):
    angle = math.atan2(y, x)
    if (angle < 0):
        angle += 2 * math.pi
    degrees = math.degrees(angle)
    return degrees

# Main loop
while True:
    # Read data from the X, Y, and Z axis registers
    x = read_data(0x03)
    z = read_data(0x05)
    y = read_data(0x07)

    # Calculate the direction
    direction = get_direction(x, y)
    print("Direction: ", direction)

    # Wait for 0.5 seconds
    time.sleep(0.5)
