
from machine import Pin, I2C
from time import sleep

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

       
addr = i2c.scan()[0]
data = bytearray(2)

while True:
    
    i2c.readfrom_mem_into(addr, 0, data)
    distance = data[0] << 8 | data[1]
    print(distance)
    
    sleep(.1)
