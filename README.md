# HopperHawk

### Current Version/Release

| Component | Version | Date |
| --------- | :-------: | :----: | 
| Hardware  | v1.4    | 03/23/2024 |
| Firmware  | v1.0    | 11/01/2024 |



### Overview
HopperHawk is an ESPHome-based smart monitoring device designed for pellet smoker enthusiasts. Using a TOF10120 time-of-flight sensor, it continuously measures the pellet level in your smoker's hopper and reports real-time fill status directly to Home Assistant. This integration enables automated low-fuel notifications, ensuring your long smoking sessions never run out of pellets unexpectedly. The device features an 18650 LiPo battery with approximately 24 hours of operational battery life, making it a reliable, wireless solution for both overnight and extended smoking sessions. HopperHawk bridges the gap between traditional smoking and smart home automation, providing peace of mind for your low-and-slow cooking adventures.

### Update Intervals
| Statistic | Frequency[^1] |
| :-------: | :-------- |
| Battery Voltage | 10 Minutes |
| Battery Remaining (%) | 10 Minutes | 
| Hopper Level | 15 Minutes |
| Pellets Remaining (%) | 15 Minutes |


[^1]: These frequencies can be customized by manually uploading the ESPHome configuration file to a fresh ESPHome install (more information is provided in the radme under the esphome directory of this repo)


# Instructions

## Initial Setup
1. Connect HopperHawk to your computer and power it on
2. Visit https://web.esphome.io and connect the device
3. Click 'Install'
4. Select the firmware
5. Click 'Install' again
6. Power cycle HopperHawk once installation completes

## Wifi Configuration
You have two options for configuring wifi:

### Option 1: Configure via ESPHome
1. On the ESPHome web interface, click the three dots menu button
2. Select "Configure Wifi"
3. Enter your wifi credentials and click connect

### Option 2: Use Configuration Portal
1. Power on HopperHawk without configured wifi
2. After 30-45 seconds, a wifi network named 'HopperHawk' will appear
   - Password: HopperHawk2024
3. Connect to this network
4. Open a web browser and navigate to http://hopperhawk.local
5. Enter your wifi credentials and click 'Save'
6. HopperHawk will connect to your home network within a few seconds

## Home Assistant Integration
### Setup
1. Ensure the ESPHome integration is installed in Home Assistant
2. Go to Settings → Devices
3. Click configure on HopperHawk
4. Click Submit
5. Click Finish

### Available Features
#### Sensors
- Battery metrics
  - Remaining life
  - Status (charging, low battery, not plugged in)
  - Voltage
- Hopper measurements
  - Empty hopper calibration (mm)
  - Full hopper calibration (mm)
  - Current hopper level (mm)
  - Calculated pellet percentage remaining

#### Control Buttons
- Calibration controls
  - Empty hopper calibration
  - Full hopper calibration
- Manual measurement refresh

## Standalone Usage
If you're not using Home Assistant, you can still access all features:

1. After connecting HopperHawk to your wifi, visit http://hopperhawk.local
2. If the address doesn't resolve, check your router for the device's IP address
3. All sensors and controls are available through the built-in web interface







