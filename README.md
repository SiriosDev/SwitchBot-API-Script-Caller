[![License][licensing-shield]](LICENSE)

# SwitchBot API Script Caller

SwitchBot API (Ver. 1.1) Script Caller, using pyscript for the scripting.

For more info click [here][switchbot-api-repo]

- [Requirements](#requirements)
- [Installation](#installation)
- [How To Use](#how-to-use)
    - [HVAC](#switchbot-hvac-api-interface)
    - [Generic Command](#switchbot-generic-command-api-interface)
- [Work in Progress](#work-in-progress)


## Requirements
- HACS
    - PyScript Integration

## Installation
1. Simply clone this repo and copy the pyscript folder in your home assisant config folder 
2. Include (or copy) [`pyscript/config.yaml`](./pyscript/config.yaml) in configuration.yaml under -> pyscript:
3. In [`pyscript/config.yaml`](./pyscript/config.yaml), set and search the following parameters (secret suggested):
    - Token (`token:`) from `Developer Option` in the SwitchBot App
    - Secret Key (`secret:`) from `Developer Option` in the SwitchBot App
    - Random Valude (`nonce:`) I suggest using an uuid generaotr, but any alphanumeric string is fine.

## How To Use
This scrypt (for now) provides two services in home assisant:

- [SwitchBot HVAC API Interface (`pyscript.switchbot_hvac`)](#switchbot-hvac-api-interface)
- [SwitchBot Generic Command API Interface (`pyscript.switchbot_generic_command`)](#switchbot-generic-command-api-interface)

### SwitchBot HVAC API Interface
Parameters:
- `deviceId:`
    - to get this id read [here][deviceid-link]
- `temperature:`
    - int value from `16` to `30`
- `mode:`
    - int value between `1` (auto), `2` (cool), `3` (dry), `4` (fan), `5` (heat)
- `fan_speed:`
    - int value between `1` (auto), `2` (low), `3` (medium), `4` (high)
- `state:`
    - string value between `on` and `off`
### SwitchBot Turn On

Parameters:
- `deviceId:`


### SwitchBot Turn Off

Parameters:
- `deviceId:`


### SwitchBot Generic Command API Interface
_For use this service read [here][generic-cmd-link]_

Parameters:
- `deviceId:`
    - to get this id read [here][deviceid-link]
- `command:`
- `parameter:` (optional)
- `commandType:`


## Work in Progress
The script works fine, but everything is still WIP, including this file.

All rights to the [API][switchbot-api-repo] belong to [OpenWonderLabs][OpenWonderLabs-lnk].

For any problems open an Issue, (soon I will insert a template for that).



[licensing-shield]: https://img.shields.io/github/license/SiriosDev/SwitchBot-API-Script-Caller?style=flat-square
[switchbot-api-repo]: https://github.com/OpenWonderLabs/SwitchBotAPI
[OpenWonderLabs-lnk]: https://github.com/OpenWonderLabs
[generic-cmd-link]: https://github.com/OpenWonderLabs/SwitchBotAPI#send-device-control-commands
[deviceid-link]: https://github.com/OpenWonderLabs/SwitchBotAPI#get-device-list
