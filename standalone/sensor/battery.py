# ========== IMPORTS ========== #
from machine import Pin, ADC
# ============================= #

# Configure Battery Voltage
battery = ADC(Pin(34, Pin.IN))
battery.atten(ADC.ATTN_11DB)
battery.width(ADC.WIDTH_12BIT)

# Configure BCM
batt_pg = Pin(25, Pin.IN, Pin.PULL_UP)
batt_s1 = Pin(27, Pin.IN, Pin.PULL_UP)
batt_s2 = Pin(26, Pin.IN, Pin.PULL_UP)

# Get the status from the battery charging controller
def get_status():
    # Grab current state
    pg = batt_pg.value()
    s1 = batt_s1.value()
    s2 = batt_s2.value()
    
    # No Input Power/Shutdown
    if pg and s1 and s2:
        return "No Input Power"
    elif not pg and not s1 and not s2:
        return "Fault"
    
    # Charging
    elif not s1 and s2 and not pg:
        return "Charging"
    
    # Charge Complete
    elif s1 and not s2 and not pg:
        return "Charge Complete"
    
    # Low Battery
    elif not s1 and s2 and pg:
        return "Low Battery"
    
    # No Battery Present
    elif s1 and s2 and not pg:
        return "No Battery Present"
    
    

# Check the battery voltage
def get_level():
    # Battery references
    max_battery_voltage = 4.0
    min_battery_voltage = 2.5
    
    # Get current voltage and estimate life remaining
    voltage = (battery.read() * (3.6/4096))*2
    voltage = voltage - (voltage*.05)

    battery_life = ((voltage - min_battery_voltage) / (max_battery_voltage - min_battery_voltage)) * 100;
    if battery_life > 100:
        return 100
    elif battery_life < 0:
        return 0
    else:
        return round(battery_life)
    

    
