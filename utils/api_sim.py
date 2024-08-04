# ===== LIBRARIES ===== #
import os, json, sys, uuid
import time, datetime
from datetime import date
from datetime import datetime
from flask import Flask, request
from waitress import serve
from flask_cors import CORS
import random
# ===================== #

# Generate random values to keep data lively
def get_status():
    battery_options = ["Charging", "Fully Charged", "No Battery Present", "Fault"]
    pellet_level = random.randrange(1,100)
    battery_level = random.randrange(1,100)
    battery_state = random.randrange(0,3)

    return (str(pellet_level) + "%"), (str(battery_level) + "%"), battery_options[battery_state]

# Output to console to verify API comms
def log(t,m):
    if logging:
        now = str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        if t == 0:
            # Failure
            print(now + " [ERROR] " + m)

        elif t == 1:
            # Success
            print(now + " [STATUS] " + m)



# API
api = Flask(__name__)

# System status
@api.route('/status', methods=['GET'])
async def api_status():
    try:
        status = get_status()
        log(1,"Returning status update with values: " + str(status))
        return json.dumps({'alive':True,'pellet_type':config['hopper']['current_pellets'],'pellet_level':status[0],'battery_level':status[1], 'battery_state':status[2]})
    except Exception as e:
        log(0,str(e))
        return json.dumps({'alive':False})

# Calibration
@api.route('/calibrate/<level>', methods=['GET','POST'])
async def api_calibrate(level):
    global config
    if request.method == 'GET':
        log(1,"GET calibration: " + str(level))
        return str(config['hopper'][(str(level)+'_measurement')])
    elif request.method == 'POST':    
        log(1,"POST calibration: " + str(level))
        if level == 'empty':
            value = random.randrange(50,100)
        else:
            value = random.randrange(10,30)

        config['hopper'][(str(level)+'_measurement')] = value
        return str(config['hopper'][(str(level)+'_measurement')])



# System reboot
@api.route('/system/<action>', methods=['POST'])
async def api_syscontrol(action):
    if action == 'reboot':
        log(1,"POST - Reboot command received")
        return "Reboot Request Received"
    if action == 'factory_reset':
        log(1,"POST - Factory reset command received")
        return "Factory Reset Request Received"

# System configuration management
@api.route('/configure/<setting>', methods=['GET','POST'])
async def api_sysconfig(setting):
    global config
    if request.method == 'GET':
        log(1,"GET Configuration for: " + str(setting))
        if setting == 'wifi':
            return json.dumps(config['wifi']), 200
        if setting == 'mqtt':
            return json.dumps(config['mqtt']), 200
        if setting == 'hopper':
            return json.dumps(config['hopper']), 200

    if request.method == 'POST':
        log(1,"POST request for: " + str(setting))
        if setting == 'wifi':
            # Load configs from POST
            config['wifi']['status'] = request.json['status']
            config['wifi']['ssid'] = request.json['ssid']
            config['wifi']['password'] = request.json['password']

            log(1,"New Wi-Fi Values: " + str(config['wifi']))

    
            return json.dumps({"configuration":"wifi"})

        if setting == 'mqtt':
            # Load configs from POST
            config['mqtt']['status'] = request.json['status']
            config['mqtt']['user'] = request.json['user']
            config['mqtt']['password'] = request.json['password']
            config['mqtt']['broker_ip'] = request.json['broker_ip']
            config['mqtt']['broker_port'] = request.json['broker_port']

            log(1,"New MQTT Values: " + str(config['mqtt']))


            return json.dumps({"configuration":"mqtt"})

        if setting == 'hopper':
            # Load configs from POST
            config['hopper']['poll_frequency'] = request.json['poll_frequency']
            config['hopper']['current_pellets'] = request.json['current_pellets']

           
            log(1,"New Hopper Values: " + str(config['hopper']))

            return json.dumps({"configuration":"hopper"})




# ===== SETUP ===== #


# Data
config = {
        'wifi': {'status':0,'ssid':"Test-SSID",'password':"MyPassword"},
        'mqtt': {'status':1,'password':"Password1234",'client_id':"hopperhawk",'broker_ip':"10.10.10.2",'broker_port':1883,'user':"svc-account"},
        'hopper': {'full_measurement':10,'empty_measurement':100,'current_pellets':"Hickory",'poll_frequency':300}
    }



# Resolve issues with CORS policy for web interface
CORS(api)
logging = True
# Start the API
serve(api, host="0.0.0.0", port=8335)