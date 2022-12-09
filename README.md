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
2. Include (or copy) [`pyscript/config.yaml`](./pyscript/config.yaml) in configuration.yaml under -> `pyscript:`
3. In [`pyscript/config.yaml`](./pyscript/config.yaml), set and search the following parameters (secret suggested):
    - Token (`token:`) from `Developer Option` in the SwitchBot App
    - Secret Key (`secret:`) from `Developer Option` in the SwitchBot App
    - Random Valude (`nonce:`) I suggest using an uuid generaotr, but any alphanumeric string is fine.

## How To Use
This scrypt creates two services in home assisant:

- [SwitchBot HVAC API Interface (`pyscript.switchbot_hvac`)](#switchbot-hvac-api-interface)
- [SwitchBot Generic Command API Interface (`pyscript.switchbot_generic_command`)](#switchbot-generic-command-api-interface)

### SwitchBot HVAC API Interface
Parameters:
- deviceId
- temperature
- mode
- fan_speed
- state

### SwitchBot Generic Command API Interface
Parameters:
- deviceId
- command
- parameter
- commandType


## Work in Progress
The script worksfine, but everything is still WIP, including this file.
For now I apologize to [OpenWonderLabs](https://github.com/OpenWonderLabs),
as soon as possible I will include all references due to the Repository.
For any problems open an Issue, (soon I will insert a template for convenience)


[licensing-shield]:https://img.shields.io/github/license/SiriosDev/SwitchBot-API-Script-Caller?style=flat-square
[switchbot-api-repo]: https://github.com/OpenWonderLabs/SwitchBotAPI
