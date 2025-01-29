## Manual Deployment

If you want to manually deploy HopperHawk you will need to flash the device with stock ESPHome firmware using either Home Assistant, the ESPHome web tool, or ESPHome CLI tools. Then you will be able to use these custom `yaml` files. Checkout [Advanced Configuration in the Wiki](https://github.com/jpecsi/hopperhawk/wiki/advanced-configuration) for instructions and details!


### Notes
- It is highly recommended to use a separate _secrets.yaml_ file to store sensitive credentials, the expected template is included
- You will need to uncomment the lines in _hopperhawk.yaml_ for wifi, ota, and api credentials if you with to add them
- The intervals for updates are in seconds
- The *tof_sensor* should update before *pellets_remaining* (by default there is a 1 second gap)
- The *battery_voltage* should update before *battery_remaining* (by default there is a 1 second gap)


