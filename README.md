# SwitchBot API Script Caller

[![License][licensing-shield]](LICENSE)



SwitchBot API (Ver. 1.1) Script Caller, using pyscript for the scripting.

For more info click [here][switchbot-api-repo]


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
This scrypt creates two services in home assisant:

- [SwitchBot HVAC API Interface (`pyscript.switchbot_hvac`)]()
- [SwitchBot Generic Command API Interface (`pyscript.switchbot_generic_command`)]()

### SwitchBot HVAC API Interface

### SwitchBot Generic Command API Interface




[licensing-shield]:https://img.shields.io/github/license/SiriosDev/SwitchBot-API-Script-Caller?style=flat-square
[switchbot-api-repo]: https://github.com/OpenWonderLabs/SwitchBotAPI