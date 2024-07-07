# ========== IMPORTS ========== #
import machine, utime, time
from machine import Pin
# ============================= #



# ========== SENSOR ========== #
# Configure Ultrasonic Sensor
scan_trigger = Pin(23, Pin.OUT)
scan_echo = Pin(22, Pin.IN)


# Take a measurement and return in cm
def take_measurement():
    
    # Trigger
    scan_trigger.value(0)
    utime.sleep_us(2)
    scan_trigger.value(1)
    utime.sleep_us(5)
    scan_trigger.value(0)

    # Wait for reading from receiver
    while scan_echo.value() == 0:
        signal_off = utime.ticks_us()
    while scan_echo.value() == 1:
        signal_on = utime.ticks_us()

    # Calculate distance in cm
    timepassed = (signal_on - signal_off)
    return ((timepassed * 0.0343) / 2)


def calibrate():
    # List to hold multiple measurements    
    measurements = []
    
    # Take several measurements and filter out junk (out of range)
    for x in range(8):
        # Take measurements
        measurements.append(take_measurement())
        
        # Pause between readings
        time.sleep(0.5) 
    
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
    # List to hold multiple measurements    
    measurements = []
    
    # Take several measurements and filter out junk (out of range)
    for x in range(8):
        m = take_measurement()
        if m >= full and m <= empty:
            measurements.append(m)
        # Pause between readings
        time.sleep(0.5) 
    
    # Get the median of the measurements
    n = len(measurements) 
    measurements.sort() 
    print(len(measurements))
    if len(measurements) >= 1:
        if n % 2 == 0: 
            median1 = measurements[n//2] 
            median2 = measurements[n//2 - 1] 
            median = (median1 + median2)/2
        else: 
            median = n_num[n//2]
        
        # Calculate the percentage remaining
        p_level = ((median-empty)*100)/(full-empty)
        
    else:
        return(-1)
    
    
        
    # Clean the result
    if p_level < 0:
        p_level = 0
    if p_level > 100:
        p_level = 100
    

    return(round(p_level))
# ============================ #








