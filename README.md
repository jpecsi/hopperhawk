# HopperHawk

*HopperHawk is an ESPHome-based smart monitoring device designed for pellet smoker enthusiasts. Using a TOF10120 time-of-flight sensor, it continuously measures the pellet level in your smoker's hopper and reports real-time fill status directly to Home Assistant. For additional information, [check out the wiki!](https://github.com/jpecsi/hopperhawk/wiki)*


### Current Version/Release

| Component | Version | Date |
| --------- | :-------: | :----: | 
| Hardware  | v1.0    | 12/12/2024 |
| Firmware  | v1.0    | 11/01/2024 |


### Update Intervals
| Statistic | Frequency[^1] |
| :-------: | :-------- |
| Battery Voltage | 10 Minutes |
| Battery Remaining (%) | 10 Minutes | 
| Hopper Level | 15 Minutes |
| Pellets Remaining (%) | 15 Minutes |


[^1]: These frequencies can be customized by manually uploading the ESPHome configuration file to a fresh ESPHome install (more information is provided in the radme under the esphome directory of this repo)






