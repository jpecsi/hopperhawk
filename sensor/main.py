# ========== IMPORTS ========== #
import network, machine, json, utime, time
import battery, sensor
import uasyncio as asyncio
from machine import Pin, ADC
from microdot_asyncio import Microdot
from umqtt.simple import MQTTClient
# ============================= #





# ========== NETWORK ========== #
def connect_network():
    if config['wifi']['status'] == 1:
        sta_if = network.WLAN(network.STA_IF)
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)
        if not sta_if.isconnected():
            sta_if.active(True)
            sta_if.config(dhcp_hostname="hopperhawk")
            sta_if.connect(config['wifi']['ssid'], config['wifi']['password'])
            while not sta_if.isconnected():
                pass
        return sta_if.ifconfig()

    else:
        ap_if = network.WLAN(network.AP_IF)
        sys_id = machine.unique_id()
        ap_ssid = "HopperHawk-" + str('{:02x}{:02x}{:02x}{:02x}'.format(machine.unique_id()[0], machine.unique_id()[1], machine.unique_id()[2], machine.unique_id()[3]))
        ap_if.active(True)
        ap_if.config(essid=ap_ssid)
        while ap_if.active() == False:
            pass
        return ap_if.ifconfig()
# ============================= #



    
        


# ========== API SERVER ========== #
# API
api = Microdot()

# System status
@api.route('/status')
async def api_status(request):
    try:
        return json.dumps({'alive':True,'pellet_level':(str(current_level)+'%'),'battery_level':(str(battery.get_level())+"%"), 'battery_state':(str(battery.get_status()))})
    except:
        return json.dumps({'alive':False})

# Calibration
@api.route('/calibrate/<level>', methods=['GET','POST'])
async def api_calibrate(request,level):
    global config
    if request.method == 'GET':
        return str(config['hopper'][(str(level)+'_measurement')])
    elif request.method == 'POST':
        config['hopper'][(str(level)+'_measurement')] = sensor.calibrate()
        with open('config.json', 'w') as f:
            json.dump(config,f)
        
        return str(config['hopper'][(str(level)+'_measurement')])

# Return current level
@api.route('/level')
async def api_measure(request):
    return str(manual_refresh()),200

# System reboot
@api.route('/system/<action>', methods=['POST'])
async def api_syscontrol(request,action):
    if action == 'reboot':
        machine.reset()

# System configuration management
@api.route('/configure/<setting>', methods=['GET','POST'])
async def api_sysconfig(request,setting):
    global config
    if request.method == 'GET':
        if setting == 'wifi':
            return json.dumps(config['wifi']), 200
        if setting == 'mqtt':
            return json.dumps(config['mqtt']), 200
        if setting == 'hopper':
            return json.dumps(config['hopper']), 200

    if request.method == 'POST':

        if setting == 'wifi':
            # Load configs from POST
            config['wifi']['status'] = request.json['status']
            config['wifi']['ssid'] = request.json['ssid']
            config['wifi']['password'] = request.json['password']
            
            # Save
            with open('config.json', 'w') as f:
                json.dump(config,f)
            
            return 'saved_wifi_settings'

        if setting == 'mqtt':
            # Load configs from POST
            config['mqtt']['status'] = request.json['status']
            config['mqtt']['user'] = request.json['user']
            config['mqtt']['password'] = request.json['password']
            config['mqtt']['broker_ip'] = request.json['broker_ip']
            config['mqtt']['broker_port'] = request.json['broker_port']

            # Save
            with open('config.json', 'w') as f:
                json.dump(config,f)

            return 'saved_mqtt_settings'

        if setting == 'hopper':
            # Load configs from POST
            config['hopper']['poll_frequency'] = request.json['poll_frequency']
            config['hopper']['current_pellets'] = request.json['current_pellets']

            # Save
            with open('config.json', 'w') as f:
                json.dump(config,f)

            return 'saved_hopper_settings'
# ================================ #





# ========== MQTT ========== #
# Push data to MQTT broker
def mqtt_publish(l,t,b,s):
    # Configure MQTT client
    client = MQTTClient('hopperhawk',config['mqtt']['broker_ip'], config['mqtt']['broker_port'], config['mqtt']['user'], config['mqtt']['password'], keepalive=60)

    # Try to connect and publish
    try:
        # Attempt the connection
        client.connect()

        # Publish the data
        client.publish('hopperhawk/pellets/level', msg=l)
        client.publish('hopperhawk/pellets/type', msg=t)
        client.publish('hopperhawk/battery/level', msg=b)
        client.publish('hopperhawk/battery/state', msg=s)

        # Wait, and disconnect
        time.sleep(.5)
        client.disconnect()

    # If it doesn't work...oh well :)
    except:
        pass
# ========================== #




# ========== SENSOR ========== #    
# Primary function to poll sensor and report data via MQTT
def sensor_routine():
    # Main loop to continuously poll/report
    while True:
        # Get the current hopper level (in cm), save globally for access via webserver
        global current_level
        m = sensor.calc_remaining(config['hopper']['empty_measurement'],config['hopper']['full_measurement'])
        if m >= 0:
            current_level = m
            
        # If MQTT is enabled, publish the data
        if config['mqtt']['status'] == 1:
            mqtt_publish(str(current_level),config['hopper']['current_pellets'], str(battery.get_level()), str(battery.get_status()))

        # Sleep for user-defined amount of time before polling again
        await asyncio.sleep(config['hopper']['poll_frequency'])

# Run when a new measurement is requested
def manual_refresh():
    global current_level
    m = sensor.calc_remaining(config['hopper']['empty_measurement'],config['hopper']['full_measurement'])
    if m >= 0:
        current_level = m
        
    # If MQTT is enabled, publish the data
    if config['mqtt']['status'] == 1:
        mqtt_publish(str(current_level),config['hopper']['current_pellets'], str(battery.get_level()), str(battery.get_status()))
        
    return current_level
    
# Push battery updates      
def push_batt_status(pin):
    if config['mqtt']['status'] == 1:
        mqtt_publish(str(current_level),config['hopper']['current_pellets'], str(battery.get_level()), str(battery.get_status()))
# ============================ #




# ========== MAIN ========== #
def start_server():
    try:
        api.run(port=80)
    except:
        api.shutdown()

async def main():
    # Run the sensor routine
    asyncio.create_task(sensor_routine())
    
    # Run the API server
    start_server()

if __name__ == '__main__':
    # Load the config file
    try:
        config = json.load(open("config.json","r"))
    except:
        config = {
            'wifi': {'status':0,'ssid':"",'password':""},
            'mqtt': {'status':0,'password':"",'client_id':"hopperhawk",'broker_ip':"",'broker_port':1883,'user':""},
            'hopper': {'full_measurement':10,'empty_measurement':75,'current_pellets':"",'poll_frequency':300}
        }
        
        with open('config.json', 'w') as f:
            json.dump(config,f)
    
    # Setup listeners for battery
    batt_pg = Pin(25, Pin.IN, Pin.PULL_UP)
    batt_s1 = Pin(26, Pin.IN, Pin.PULL_UP)
    batt_s2 = Pin(27, Pin.IN, Pin.PULL_UP)
    batt_pg.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING, handler = push_batt_status)
    batt_s1.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING, handler = push_batt_status)
    batt_s2.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING, handler = push_batt_status)

    # Working variables
    current_level = 0
    
    # Configure the network
    status = connect_network()

    # Start
    asyncio.run(main())
# ========================== #









