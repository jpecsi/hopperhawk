# ========== IMPORTS ========== #
import random
# ============================= #

# Get the status from the battery charging controller
def get_status():
    # Possible battery states
    battery_states = ['No Input Power', 'Fault', 'Charging', 'Charge Complete', 'Low Battery', 'No Battery Present']
    return battery_states[random.randint(0,5)]
    
    

# Check the battery voltage
def get_level():
    # Battery references
    min_battery_voltage = 2
    max_battery_voltage = 4

    # Get current voltage and estimate life remaining
    voltage = round((random.randint(min_battery_voltage,max_battery_voltage)+random.random()),2)

    battery_life = ((voltage - min_battery_voltage) / (max_battery_voltage - min_battery_voltage)) * 100;
    if battery_life > 100:
        return 100
    elif battery_life < 0:
        return 0
    else:
        return round(battery_life)
    

    
