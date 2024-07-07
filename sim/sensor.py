# ========== IMPORTS ========== #
from time import sleep
import random
# ============================= #

# Scoping for simulator
# Sensor can measure 10cm to 180cm
SENSOR_MAX = 180
SENSOR_MIN = 10


# =========== SENSOR ========== #
# Take a measurement and return in cm
def take_measurement():
    return round((random.randint(SENSOR_MIN,SENSOR_MAX)+random.random()),2)

def calibrate(level):
    if level == 'empty':
        return round((random.randint((SENSOR_MAX-25),SENSOR_MAX)+random.random()),2)
    elif level == 'full':
        return round((random.randint(SENSOR_MIN,(SENSOR_MIN+25))+random.random()),2)

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








