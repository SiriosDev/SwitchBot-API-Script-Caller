[![License][licensing-shield-this]](LICENSE) <br>
All rights to the [API][switchbot-api-repo] belong to [OpenWonderLabs][openwonderlabs-lnk].

# SwitchBot API Script Caller (v 0.3)

This (Py)Script allows you to control all (WIP) your SwitchBot devices via API calls (1.1).

> **Warning** <br>
> At the moment not all API-compatible models are implemented, if you have the capability do a [fork][fork] and implement it (and request a [PR][pr]), otherwise open an [issue][issues] with "TEST|**_Model_Name_**" in the title.

For more info click [here][switchbot-api-repo]

- [Requirements](#requirements)
- [Installation](#installation)
- [How To Use](#how-to-use)
  - [Refresh Devices](#switchbot-refresh-devices)
  - [Get Status](#switchbot-get-status)
  - [Turn On](#switchbot-turn-on)
  - [Turn Off](#switchbot-turn-off)
  - [Bot](#switchbot-bot-control)
  - [Curtain](#switchbot-curtain-control)
  - [HVAC](#switchbot-ir-hvac-control)
  - [Light](#switchbot-ir-light-control)
  - [Generic Command](#switchbot-generic-command)
- [Work in Progress](#work-in-progress)
- [Changelog](#changelog)

## Requirements

- HACS ([docs][hacs-docs])
  - PyScript Integration ([docs][pyscript-docs])

## Installation

⚠️ **If you update from one of the following versions there have been breaking changes:**

<details>
<summary>Versions</summary>

- [Unnumbered (2023.01.14)][unnum]

</details>

### Procedure

1. **Clone this repository in your config folder**
   ```sh
   cd /config
   git clone https://github.com/SiriosDev/SwitchBot-API-Script-Caller.git
   ```
2. **Check if you have a `pyscript/config.yaml` file. If not, create one and then add the following in your main top-level configuration.yaml file.**
   ```yaml
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
The project is still under development, and breaking changes may **frequently** occur.

### Installation Notes

- In order to see the `Developer options` in the Switchbot app (version ≥6.14), click repetively on the version number in the App's settings.
    <details>
    <summary>Click here for detailed procedure</summary>

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
- [SwitchBot Get Status (`pyscript.switchbot_get_status`)](#switchbot-get-status)
- [SwitchBot Turn ON (`pyscript.switchbot_turn_on`)](#switchbot-turn-on)
- [SwitchBot Turn OFF (`pyscript.switchbot_turn_off`)](#switchbot-turn-off)
- [SwitchBot Bot Control (`pyscript.switchbot_curtain_command`)](#switchbot-bot-control)
- [SwitchBot Curtain Control (`pyscript.switchbot_curtain_command`)](#switchbot-curtain-control)
- [SwitchBot IR HVAC Control (`pyscript.switchbot_hvac`)](#switchbot-ir-hvac-control)
- [SwitchBot IR Light Control (`pyscript.switchbot_ir_light_control`)](#switchbot-ir-light-control)
- [SwitchBot Generic Command (`pyscript.switchbot_generic_command`)](#switchbot-generic-command)

### 🔸SwitchBot Refresh Devices

_Creates Home Assistant entity with the best type-domain association, otherwise with domain `switch`. These devices are stored as `<entity_type>.switchbot_remote_<device*name>`eg: A SwitchBot Curtain™ will become`cover.switchbot_remote_bedroom_curtains`*

_The `<device_name>` corresponds to the name of the device in the SwitchBot app._  
_If `<device_name>` doesn't contains Alphanum characters (e.g is written in another alphabet), it is replaced by `<deviceType>_<deviceId[-4:]>`(e.g.`switch.switchbot*remote_light_0D62`)*  
_The `<deviceId>` is an internal unique code._  
**_⚠️The entities can then be used for sending commands or getting status using other functions of this pyscript.⚠️_** </br>
**_⚠️ Not working stand alone ⚠️_**</br>
_If this service does not find all the devices it had previously found, it will alert you with a persistent notification in the HA WebUi._

Parameters: **_None_**

### 🔸Switchbot Get Status

_Gets the state of Switchbot Bots, Contact Sensors, Curtains and Meters._
Runs every five minutes generating 288 API calls per sensor per day. Switchbot limits API calls to 10,000 per day. So, this limits the number of devices to 34 (excluding IR devices.) See the [SwitchbotAPI API](<[url](https://github.com/OpenWonderLabs/SwitchBotAPI#get-device-status)>) for the data returned from a status call.

Parameters: **_None_**

### 🔸SwitchBot Turn On

_Turn a device ON._

Parameters:

- `device`
  - See [`SwitchBot Refresh Devices`](#switchbot-refresh-devices).

### 🔸SwitchBot Turn Off

_Turn a device OFF._

Parameters:

- `device`
  - See [`SwitchBot Refresh Devices`](#switchbot-refresh-devices).

### 🔸SwitchBot Bot Control

_Interface for "Classic" Bot (turnOn, turnOff, press) devices._

**Parameters:**

- `device`
  - See [`SwitchBot Refresh Devices`](#switchbot-refresh-devices).
- `command:`
  - string value between `turnOn`, `turnOff`, `press`
- `repetition:`
  - int value from `1` to `10`, _only works with `press`_, iterates the command as many times as selected.

### 🔸Switchbot Curtain Control

_Interface for Curtain (turnOn, turnOff, setPosition) devices._

- `device`
  - See [`SwitchBot Refresh Devices`](#switchbot-refresh-devices).
- `command:`
  - string value between `turnOn`, `turnOff`, `setPosition`
- `index:`
  - [wip] int value between `?????` (required for "setPosition" command, otherwise it will be ignored)
- `mode:`
  - string value between `Performance`, `Silent`, `Default` (required for "setPosition" command, otherwise it will be ignored)
- `position:`
  - int value (in percentage) between `0` and `100` (required for "setPosition" command, otherwise it will be ignored)

### 🔸SwitchBot IR HVAC Control

_Interface for infrared HVAC (heating, ventilation and air conditioning) devices._

**Parameters:**

- `device`
  - See [`SwitchBot Refresh Devices`](#switchbot-refresh-devices).
- `state:`
  - string value between `on` and `off`
- `temperature:`
  - int value from `16` to `30`
- `mode:`
  - string value between `Auto`, `Cool`, `Dry`, `Fan`, `Heat`
- `fan_speed:`
  - int value between `Auto`, `Low`, `Medium`, `High`

### 🔸SwitchBot IR Light Control

_Interface for infrared Light (turnOn, turnOff, brightnessUp and brightnessDown) devices._

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

## Work in Progress

The script works fine, but everything is still WIP, including this file.
For any problems open an Issue, (soon I will insert a template for that).

## Changelog

### <Release date> v? (🟢 New Features)

**Add support for non-IR devices** : Bot, Contact Sensor, Curtain and Meter.

**Add service 'Switchbot Curtains Command'** : Send command to Curtain device.

**Add time trigger to get the status of Bots, Contact Sensors, Curtains and Meters every 5 minutes.** This will show in the Logbook even if you only have IR devices. However, the API calls will only be made for non-IR devices.

**Add time trigger to run 'Refresh Devices' at startup.**

### 2023.02.19 v0.2.1 (🛠️ Some Fixes)

**Fixed ([#15][i15]) `commandType` parameters in `Generic Command`**.<br>
_Suggest updating if you need to control custom remotes created in the mobile app_.

### 2023.01.16 v0.2.0 (🟢 New Features and 🛠️ Some Fixes)

**Add service `SwitchBot IR Light Control`**:<br>
Send command via infrared to light device.

**Corrected some descriptions**.

**Reworked the way `Refresh Devices` assigns `Friendly Names`**.

**Removed notifications to all channels in case of errors during `Refresh Devices`**.

**Now HVAC will have a dedicated icon once the dummy switch is created (`Refresh Devices`)**.

**Renamed `SwitchBot HVAC API Interface` in `SwitchBot IR HVAC Control`**: _it doesn't affect function it's just a visual thing_.

**Renamed `SwitchBot Generic Command API Interface` in `SwitchBot Generic Command`**: _it doesn't affect function it's just a visual thing_.

### 2023.01.14 v0.1.0 (⚠️ Breaking changes)

**Add service `SwitchBot Refresh Devices`**:<br>
Retrieves your IR devices from the API. Services now requires `device` instead of `deviceId`. No need to copy paste the id manually anymore.

Previously:

- Services param was `deviceId`

Now:

- Services Param is `device` (home assistant ID for sensor, e.g. `switch.switchbot_remote_my_light`)

Make sure to run `SwitchBot Refresh Devices` before configuring anything else.

[Full Changelog History here][changelog]

[licensing-shield-this]: https://img.shields.io/github/license/SiriosDev/SwitchBot-API-Script-Caller?style=flat-square
[licensing-shield-ps]: https://img.shields.io/github/license/custom-components/pyscript?style=flat-square
[licensing-shield-sbapi]: https://img.shields.io/github/license/OpenWonderLabs/SwitchBotAPI?style=flat-square
[licensing-shield-hass]: https://img.shields.io/github/license/home-assistant/core?style=flat-square
[hacs-docs]: https://hacs.xyz/docs/setup/prerequisites
[pyscript-docs]: https://hacs-pyscript.readthedocs.io/en/latest/installation.html
[switchbot-api-repo]: https://github.com/OpenWonderLabs/SwitchBotAPI
[openwonderlabs-lnk]: https://github.com/OpenWonderLabs
[generic-cmd-link]: https://github.com/OpenWonderLabs/SwitchBotAPI#send-device-control-commands
[deviceid-link]: https://github.com/OpenWonderLabs/SwitchBotAPI#get-device-list
[issues]: https://github.com/SiriosDev/SwitchBot-API-Script-Caller/issues/new
[pr]: https://github.com/SiriosDev/SwitchBot-API-Script-Caller/pulls
[fork]: https://github.com/SiriosDev/SwitchBot-API-Script-Caller/fork
[changelog]: CHANGELOG.md
[i15]: https://github.com/SiriosDev/SwitchBot-API-Script-Caller/issues/15
[unnum]: #20230114-v010-%EF%B8%8F-breaking-changes

---

**SwitchBot API Script Caller** is an unofficial, community-driven script NOT affiliated, endorsed or supported by **Wonderlabs, Inc.** Some images used in this app are copyrighted and are supported under fair use. **SwitchBot** and **SwitchBot model names** are trademarks of **Wonderlabs**. No copyright infringement intended. <br>
**© SwitchBot Global.** <br>
**© Wonderlabs.**

---

PyScript is distributed under [![License][licensing-shield-ps]](https://github.com/custom-components/pyscript)license.<br>
The APIs are distributed under [![License][licensing-shield-sbapi]][switchbot-api-repo]  license.<br>
HomeAssistant is distributed under [![License][licensing-shield-hass]](https://github.com/home-assistant/core) license.<br>

***The License at the top of this document refers only to the code in this repository***

---