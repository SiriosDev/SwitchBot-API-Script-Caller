# Changelog
## 2023.02.19 v0.2.1 (🛠️ Some Fixes)

**Fixed (#15) `commandType` parameters in `Generic Command`**.<br>
*Suggest updating if you need to control custom remotes created in the mobile app*.



## 2023.01.16 v0.2.0 (🟢 New Features and 🛠️ Some Fixes)
**Add service `SwitchBot IR Light Control`**:<br>
 Send command via infrared to light device.

**Corrected some descriptions**.

**Reworked the way `Refresh Devices` assigns `Friendly Names`**.

**Removed notifications to all channels in case of errors during `Refresh Devices`**.

**Now HVAC will have a dedicated icon once the dummy switch is created (`Refresh Devices`)**.

**Renamed `SwitchBot HVAC API Interface` in `SwitchBot IR HVAC Control`**: _it doesn't affect function it's just a visual thing_.

**Renamed `SwitchBot Generic Command API Interface` in `SwitchBot Generic Command`**: _it doesn't affect function it's just a visual thing_.


## 2023.01.14 v0.1.0 (⚠️ Breaking changes)
**Add service `SwitchBot Refresh Devices`**:<br>
Retrieves your IR devices from the API. Services now requires `device` instead of `deviceId`. No need to copy paste the id manually anymore.

Previously:
  - Services param was `deviceId`
 
Now:
  - Services Param is `device` (home assistant ID for sensor, e.g. `switch.switchbot_remote_my_light`)  
 
Make sure to run `SwitchBot Refresh Devices` before configuring anything else.

## 2023.01.05 (🟢 2 New Features)
**Add Service `SwitchBot Turn On`**  
**Add Service `SwitchBot Turn Off`**

The `turn<On/Off>` services allow you to switch On and Off your device with a simple command requiring only the deviceId.
Almost all devices are compatible with this command according to the API documentation.

## Before (🟢 2 New Features)
**Add Service `SwitchBot HVAC API Interface`**  
**Add Service `SwitchBot Generic Command API Interface`**