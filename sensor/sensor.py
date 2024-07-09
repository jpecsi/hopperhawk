# ========== IMPORTS ========== #
from machine import Pin, I2C
from time import sleep
# ============================= #



# =========== SENSOR ========== #
# Configure TOF10120 Sensor 
sensor_i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
sensor_addr = sensor_i2c.scan()[0]
sensor_data = bytearray(2)

# Take a measurement and return in cm
def take_measurement():
    # List to hold multiple measurements    
    measurements = []
    
    # Take several measurements and filter out junk (out of range)
    for x in range(8):
        # Take measurements
        sensor_i2c.readfrom_mem_into(sensor_addr, 0, sensor_data)
        measurements.append(sensor_data[0] << 8 | sensor_data[1])
        
        # Pause between readings
        sleep(0.1) 
    
    # Get the median of the measurements
    n = len(measurements) 
    measurements.sort() 
     
    if n % 2 == 0: 
        median1 = measurements[n//2] 
        median2 = measurements[n//2 - 1] 
        median = (median1 + median2)/2
    else: 
        median = n_num[n//2] 

    return(median)


# Calculate remaining pellets
def calc_remaining(empty,full):
    # Calculate the percentage
    p_level = ((take_measurement()-empty)*100)/(full-empty)
        
    # Clean the result
    if p_level < 0:
        p_level = 0
    if p_level > 100:
        p_level = 100
    

    return(round(p_level))
# ============================= #








