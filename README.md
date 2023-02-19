[![License][licensing-shield]](LICENSE)
All rights to the [API][switchbot-api-repo] belong to [OpenWonderLabs][OpenWonderLabs-lnk].

# SwitchBot API Script Caller (v 0.2.0)

This (Py)Script allows you to control all (WIP) your SwitchBot devices via API calls (1.1).

‼️‼️At the moment we have implemented all the devices that we can test, so if you want to be a tester please open an [issue][issues] with "test" in the title or if you are also able to develop go ahead and do a [PR][pr]‼️‼️

For more info click [here][switchbot-api-repo]

- [Requirements](#requirements)
- [Installation](#installation)
- [How To Use](#how-to-use)
    - [Refresh Devices](#switchbot-refresh-devices)
    - [Turn On](#switchbot-turn-on)
    - [Turn Off](#switchbot-turn-off)
    - [HVAC](#switchbot-hvac-api-interface)
    - [Light](#switchbot-ir-light-control)
    - [Generic Command](#switchbot-generic-command-api-interface)
    - [Curtain](#switchbot-curtain-control)
    - [Get Status](#switchbot-get status)
- [Work in Progress](#work-in-progress)
- [Changelog](#changelog)

## Requirements

- HACS ([docs][hacs-docs])
    - PyScript Integration ([docs][pyscript-docs])
      
## Installation
### Procedure
1. **Clone this repository in your config folder**
   ```sh
   cd /config
   git clone https://github.com/SiriosDev/SwitchBot-API-Script-Caller.git
   ```
2. **Check if you have a `pyscript/config.yaml` file. If not, create one and then add the following in your main top-level configuration.yaml file.**
    ``` yaml
    pyscript: !include pyscript/config.yaml
    ```
3. **Include [`pyscript/switchbot.yaml`](./pyscript/switchbot.yaml) in your `pyscript/config.yaml` under the `switchbot` section**
   ```yaml
   # /config/pyscript/config.yaml
   allow_all_imports: true
   apps:
   # (...)
   # ↓↓↓ attention indentation
    switchbot: !include /config/SwitchBot-API-Script-Caller/pyscript/switchbot.yaml
   # (...)
   ```
4. **Set the authentication secrets in `secrets.yaml` homeassistant file**
    - Random Value (`switchbot_nonc`) (I suggest using an UUID generator, but any unique alphanumeric string is fine)
    ```yaml
    # secrets.yaml
    # (...)
    # Token and Secret Key : from `Developer Option` in the SwitchBot App (version ≥6.14)
    switchbot_token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    switchbot_sec: xxxxxxxxxxxx
    # Random Value: you can use a UUID generator, but any unique alphanumeric string is OK
    switchbot_nonc: xxxxxxxxxx
    ```
5. **Link the files in the `pyscript` directory**
   ```sh
   # use `mkdir -p /config/pyscript/apps/` if the directory doesn't exist
   cd /config/pyscript/apps/
   
   # Create a symbolic link to the apps directory named switchbot
   ln -s /config/SwitchBot-API-Script-Caller/pyscript/apps/switchbot.py switchbot.py
   ```
   
### Further Update
By following this procedure, the script can then be updated with newer version using git.
```sh
cd SwitchBot-API-Script-Caller
git pull
```
⚠️ **See changelog before updating.**  
The project is still in development and breaking changes may occurs.

### Installation Notes
- In order to see the `Developer options` in the Switchbot app (version ≥6.14), click repetively on the version number in the App's settings.
    <details>
    <summary>Click her for detailed procedure</summary>
  
  ![SwitchBot](https://user-images.githubusercontent.com/26876994/210898538-5d07a304-3446-48e0-b020-69140ba89b45.png)
  
    </details>
- A symbolic link is symbolic and represent the exact path you enter, if you move the targeted file or if the target is outside of the container (e.g. when using docker) the link will not work. Make sure that you are using a relative path that is accessible for the host reading the link. 
- Ensure that `pyscript` is operational before to install this script.
- Except dirs strictly related to pyscript, all others dir are recommended, so organize them as you like, keeping in mind that changing the contents of the "`clone`", could cause the update via `git pull` to fail.

## How To Use
This script (for now) provides the following services in home assisant.
It is important to execute [`SwitchBot Refresh Devices`](#switchbot-refresh-devices) first in order to be able to use the other features, as it will generate the required Home Assistant entities for your devices.

### Summary
- [SwitchBot Refresh Devices (`pyscript.switchbot_refresh_devices`)](#switchbot-refresh-devices)
- [SwitchBot Turn ON (`pyscript.switchbot_turn_on`)](#switchbot-turn-on)
- [SwitchBot Turn OFF (`pyscript.switchbot_turn_off`)](#switchbot-turn-off)
- [SwitchBot IR HVAC Control (`pyscript.switchbot_hvac`)](#switchbot-hvac-api-interface)
- [SwitchBot IR Light Control (`pyscript.switchbot_ir_light_control`)](#switchbot-ir-light-control)
- [SwitchBot Generic Command (`pyscript.switchbot_generic_command`)](#switchbot-generic-command-api-interface)
- [SwitchBot Curtain Command (`pyscript.switchbot_curtain_command`)](#switchbot-curtain-control)
- [SwitchBot Get Status (`pyscript.switchbot_get_status`)](#switchbot-get-status)

### 🔸SwitchBot Refresh Devices
_Creates Home Assistant `switch` entity for each IR Device and Bot connected to your SwitchBot Hub. IR devices and Bots are stored as `switch.switchbot_remote_<device_name>`._  
_Creates Home Assistant `cover` entity for each Curtain, `binary_sensor` entity for each Contact Sensor and `sensor` entity for each Meter connected to your Switchbot Hub. These devices are stored as `<entity_type>.switchbot_remote_<device_name>` eg `cover.switchbot_remote_bedroom_curtains`_

_`<device_name>` corresponds to the name of the device in the SwitchBot app._  
_If `<device_name>` doesn't contains Alphanum characters (e.g is written in another alphabet), it is replaced by `<deviceType>_<deviceId[-4:]>` (e.g. `switch.switchbot_remote_light_0D62`)_  
_The entities can then be used for sending commands or getting status using other functions of this pyscript. ⚠️ Not working stand alone ⚠️_
_In case the device doesn't exist in the future, you will be notified on your devices._

Parameters: ***None***

### 🔸SwitchBot Turn On
_Turn a device ON_

Parameters:
- `device`
    - See [`SwitchBot Refresh Devices`](#switchbot-refresh-devices).

### 🔸SwitchBot Turn Off
_Turn a device OFF_

Parameters:
- `device`
    - See [`SwitchBot Refresh Devices`](#switchbot-refresh-devices).

### 🔸SwitchBot IR HVAC Control
_Interface for infrared HVAC (heating, ventilation and air conditioning) device._

**Parameters:**
- `device`
    - See [`SwitchBot Refresh Devices`](#switchbot-refresh-devices).
- `temperature:`
    - int value from `16` to `30`
- `mode:`
    - int value between `1` (auto), `2` (cool), `3` (dry), `4` (fan), `5` (heat)
- `fan_speed:`
    - int value between `1` (auto), `2` (low), `3` (medium), `4` (high)
- `state:`
    - string value between `on` and `off`


### 🔸SwitchBot IR Light Control
_Interface for infrared Light (turnOn, turnOff, brightnessUp and brightnessDown) device._

**Parameters:**
- `device`
    - See [`SwitchBot Refresh Devices`](#switchbot-refresh-devices).
- `command:`
    - string value between `turnOn`, `turnOff`, `brightnessUp` and `brightnessDown`
- `steps:`
    - int value from `1` to `10`, _only works with `brightnessUp/Down`_, iterates the command as many times as selected.


### 🔸SwitchBot Generic Command
_Allows you to send any request to the API. (See [documentation][generic-cmd-link])_

**Parameters:**
- `device`
    - See [`SwitchBot Refresh Devices`](#switchbot-refresh-devices).
- `command:`
    - One of the commands supported by the device. (see [documentation][generic-cmd-link])
- `parameter:` (optional)
    - Parameter for the command, if required (e.g. `SetChannel`)
    - use `default` if not used
- `commandType:`
    - `command` for standard commands
    - `customize` for custom commands

### 🔸Switchbot Curtain Control
_Interface for Curtain (turnOn, turnOff, setPosition)_
- `device`
    - See [`SwitchBot Refresh Devices`](#switchbot-refresh-devices).
- `command:`
    - string value between `turnOn`, `turnOff`, `setPosition`
- `parameter:` (optional)
    - string giving the position for the setPosition command. (See the [SwitchbotAPI Curtain command]([url](https://github.com/OpenWonderLabs/SwitchBotAPI#curtain-2)).)
    
### 🔸Switchbot Get Status
_Gets the state of Switchbot Bots, Contact Sensors, Curtains and Meters._
Runs every five minutes generating 288 API calls per sensor per day. Switchbot limits API calls to 10,000 per day. So, this limits the number of devices to 34 (excluding IR devices.) See the [SwitchbotAPI API]([url](https://github.com/OpenWonderLabs/SwitchBotAPI#get-device-status)) for the data returned from a status call.

Parameters: ***None***


## Work in Progress
The script works fine, but everything is still WIP, including this file.
For any problems open an Issue, (soon I will insert a template for that).


## Changelog
### <Release date> v? (🟢 New Features)
**Add support for non-IR devices** : Bot, Contact Sensor, Curtain and Meter.

**Add service 'Switchbot Curtains Command'** : Send command to Curtain device.

**Add time trigger to get the status of Bots, Contact Sensors, Curtains and Meters every 5 minutes.** This will show in the Logbook even if you only have IR devices. However, the API calls will only be made for non-IR devices.

**Add time trigger to run 'Refresh Devices' at startup.**

### 2023.01.16 v0.2.0 (🟢 New Features and 🛠️ some fixes)
**Add service `SwitchBot IR Light Control`** : Send command via infrared to light device.

**Corrected some descriptions**.

**Reworked the way `Refresh Devices` assigns `Friendly Names`**.

**Removed notifications to all channels in case of errors during `Refresh Devices`**.

**Now HVAC will have a dedicated icon once the dummy switch is created (`Refresh Devices`)**.

**Renamed `SwitchBot HVAC API Interface` in `SwitchBot IR HVAC Control`**: _it doesn't affect function it's just a visual thing_.

**Renamed `SwitchBot Generic Command API Interface` in `SwitchBot Generic Command`**: _it doesn't affect function it's just a visual thing_.


### 2023.01.14 v0.1.0 (⚠️ Breaking changes)
**Add service `SwitchBot Refresh Devices`** : Retrieves your IR devices from the API. Services now requires `device` instead of `deviceId`. No need to copy paste the id manually anymore.

Previously:  
  - Services param was `deviceId`
 
Now:
  - Services Param is `device` (home assistant ID for sensor, e.g. `switch.switchbot_remote_my_light`)  
 
Make sure to run `SwitchBot Refresh Devices` before configuring anything else.

### 2023.01.05 (🟢 2 New Features)
**Add Service `SwitchBot Turn On`**  
**Add Service `SwitchBot Turn Off`**

The `turn<On/Off>` services allow you to switch On and Off your device with a simple command requiring only the deviceId.
Almost all devices are compatible with this command according to the API documentation.

### Before (🟢 2 New Features)
**Add Service `SwitchBot HVAC API Interface`**  
**Add Service `SwitchBot Generic Command API Interface`**


[licensing-shield]: https://img.shields.io/github/license/SiriosDev/SwitchBot-API-Script-Caller?style=flat-square
[hacs-docs]: https://hacs.xyz/docs/setup/prerequisites
[pyscript-docs]: https://hacs-pyscript.readthedocs.io/en/latest/installation.html
[switchbot-api-repo]: https://github.com/OpenWonderLabs/SwitchBotAPI
[OpenWonderLabs-lnk]: https://github.com/OpenWonderLabs
[generic-cmd-link]: https://github.com/OpenWonderLabs/SwitchBotAPI#send-device-control-commands
[deviceid-link]: https://github.com/OpenWonderLabs/SwitchBotAPI#get-device-list
[issues]: https://github.com/SiriosDev/SwitchBot-API-Script-Caller/issues/new
[pr]: https://github.com/SiriosDev/SwitchBot-API-Script-Caller/pulls
