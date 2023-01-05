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
- HACS ([docs](https://hacs.xyz/docs/setup/prerequisites))
    - PyScript Integration ([docs](https://hacs-pyscript.readthedocs.io/en/latest/installation.html))
      

## Installation
### Procedure
1. **Clone this repository in your config folder**
   ```sh
   cd /config
   git clone https://github.com/SiriosDev/SwitchBot-API-Script-Caller.git
   ```
2. **Include [`pyscript/switchbot.yaml`](./pyscript/switchbot.yaml) in your `pyscript/config.yaml` under the `switchbot` section**
   ```yaml
   # /config/pyscript/config.yaml
   allow_all_imports: true
   apps:
   # (...)
   # ↓↓↓ attention indentation
    switchbot: !include /config/SwitchBot-API-Script-Caller/pyscript/switchbot.yaml
   # (...)
   ```
3. **Set the authentication secrets in `secrets.yaml` homeassistant file**
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
4. **Link the files in the `pyscript` directory**
   ```sh
   # use `mkdir -p /config/pyscript/apps/` if the directory doesn't exist
   cd /config/pyscript/apps/
   
   # Create a symbolic link to the apps directory named switchbot
   ln -s /config/SwitchBot-API-Script-Caller/pyscript/apps switchbot
   ```
   
### Further Update
By following this procedure, the script can then be updated with newer version using git.
```sh
cd SwitchBot-API-Script-Caller
git pull
```

### Installation Notes
- In order to see the `Developper options` in the Switchbot app (version ≥6.14), click repetively on the version number in the App's settings
- A symbolic link is symbolic and represent the exact path you enter, if you move the targeted file or if the target is outside of the container (e.g. when using docker) the link will not work. Make sure that you are using a relative path that is accessible for the host reading the link. 
- Ensure that `pyscript` is operational before to install this script.

## How To Use
This script (for now) provides two services in home assisant:

### Summary
- [SwitchBot HVAC API Interface (`pyscript.switchbot_hvac`)](#switchbot-hvac-api-interface)
- [SwitchBot Generic Command API Interface (`pyscript.switchbot_generic_command`)](#switchbot-generic-command-api-interface)

### SwitchBot HVAC API Interface
_Interface for infrared HVAC (heating, ventilation and air conditioning) device._

**Parameters:**
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

### SwitchBot Generic Command API Interface
_Allows you to send any request to the API. (See [documentation][generic-cmd-link])_

**Parameters:**
- `deviceId:`
    - to get this id read [here][deviceid-link]
- `command:`
    - One of the command supported by the device. (see [documentation][generic-cmd-link])
- `parameter:`
    - Parameter for the command, if required (e.g. SetChannel)
    - use "default" if not used
- `commandType:`
    - `command` for standard commands
    - `customize` for others


## Work in Progress
The script works fine, but everything is still WIP, including this file.

All rights to the [API][switchbot-api-repo] belong to [OpenWonderLabs][OpenWonderLabs-lnk].

For any problems open an Issue, (soon I will insert a template for that).



[licensing-shield]: https://img.shields.io/github/license/SiriosDev/SwitchBot-API-Script-Caller?style=flat-square
[switchbot-api-repo]: https://github.com/OpenWonderLabs/SwitchBotAPI
[OpenWonderLabs-lnk]: https://github.com/OpenWonderLabs
[generic-cmd-link]: https://github.com/OpenWonderLabs/SwitchBotAPI#send-device-control-commands
[deviceid-link]: https://github.com/OpenWonderLabs/SwitchBotAPI#get-device-list
