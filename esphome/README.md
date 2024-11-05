## Manual Deployment

If you want to manually deploy HopperHawk you will need to flash the device with stock ESPHome firmware using either Home Assistant, the ESPHome web tool, or ESPHome CLI tools.

### When to use this
1. Building your own hardware
2. Want to customize the update intervals
3. Want to enable ota/api passwords and encryption
4. Want to modify/customize functionality


### Notes
- It is highly recommended to use a separate _secrets.yaml_ file to store sensitive credentials, the expected template is included
- You will need to uncomment the lines in _hopperhawk.yaml_ for wifi, ota, and api credentials if you with to add them
- The intervals for updates are in seconds
- The *tof_sensor* should update before *pellets_remaining* (by default there is a 1 second gap)
- The *battery_voltage* should update before *battery_remaining* (by default there is a 1 second gap)

## Instructions

*These steps assume you have Home Assistant up and running, and the ESPHome add-on installed*

1. Connect HopperHawk to your computer and power it on
2. Visit https://web.esphome.io and connect the device
3. Click 'Prepare For First Use'
4. Click 'Install'
6. Power cycle HopperHawk once installation completes
7. On the ESPHome web interface, click the three dots menu button
8. Select "Configure Wifi"
9. Enter your wifi credentials and click connect
10. Go to the ESPHome Dashbord in Home Assistant and adopt the new device
11. Configure your **secrets** file in Home Assistant to match the format [provided here](https://github.com/jpecsi/hopperhawk/blob/main/esphome/secrets.yaml)
12. Upload or copy/paste the contents of [hopperhawk.yaml](https://github.com/jpecsi/hopperhawk/blob/main/esphome/hopperhawk.yaml) into the configuration for the device and apply




