import time, hashlib, hmac, base64, requests

# "input" from config
def auth(token=None, secret=None, nonce=None):

    token=str(token)
    secret=str(secret)
    nonce=str(nonce)
    
    t = int(round(time.time() * 1000))
    string_to_sign = '{}{}{}'.format(token, t, nonce)

    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret = bytes(secret, 'utf-8')

    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

    h={"Authorization": (str(token)), "t": (str(t)), "sign": (str(sign, 'utf-8')), "nonce": (str(nonce)), "Content-Type": "application/json; charset=utf8"}
    return h

@pyscript_executor
def requestHelper(_url,_json,_headers):
    x=requests.post(_url,json = _json, headers=_headers)

#services
@service
def switchbot_hvac(deviceId, temperature, mode, fan_speed, state):
    """yaml
name: SwitchBot HVAC API Interface
description: This (py)script allows you to control HVAC "saved" in "Switchbot Mini Hub" (or other switchbot brand ir blasters !! not yet tested !!).
fields:
  deviceId:
    name: Device ID
    description: HVAC Target device id (get req. to api)
    example: 00-000000000000-00000000
    default:
    required: true
    selector:
      text:

  temperature:
    name: Temperature
    description: HVAC Target Temperature in Celsius (min 16 - Max 30)
    example: 26
    default:
    required: true
    selector:
      number:
        min: 16
        max: 30
        step: 1
        unit_of_measurement: "°C"
        mode: box

  mode:
    name: Mode
    description: HVAC Mode Selector 1 (auto), 2 (cool), 3 (dry), 4 (fan), 5 (heat)
    example: 1
    default:
    required: true
    selector:
      number:
        min: 1
        max: 5
        step: 1
        mode: box

  fan_speed:
    name: Fan Speed
    description: HVAC Fan Speed Selector 1 (auto), 2 (low), 3 (medium), 4 (high)
    example: 1
    default:
    required: true
    selector:
      number:
        min: 1
        max: 4
        step: 1
        mode: box

  state:
    name: Power State
    description: HVAC Power State
    example: off
    default:
    required: true
    selector:
      select:
        options:
          - on
          - off
        mode: list
      """
    headers_dict=auth(**pyscript.app_config)
        
    url=f"https://api.switch-bot.com/v1.1/devices/{deviceId}/commands"
    myjson= {"command": "setAll","parameter": f"{temperature},{mode},{fan_speed},{state}","commandType": "command"}
    requestHelper(url,myjson,headers_dict)

@service
def switchbot_generic_command(deviceId, command, parameter, commandType):
    """yaml
name: SwitchBot Generic Command API Interface
description: This (py)script allows you to control all device in your "Switchbot Home" (refer to https://github.com/OpenWonderLabs/SwitchBotAPI)
fields:
  deviceId:
    name: Device ID
    description: Target deviceId (get req. to api)
    example: 00-000000000000-00000000
    default:
    required: true
    selector:
      text:

  command:
    name: Command
    description: the name of the command
    example: turnOff
    default: turnOff
    required: true
    selector:
      text:

  parameter:
    name: Parameters
    description: some commands require parameters, such as SetChannel
    example: default
    default: default
    required: true
    selector:
      text:

  commandType:
    name: Command Type
    description: for customized buttons, this needs to be set to customzie
    example: command
    default: command
    required: true
    selector:
      text:

      """
    headers_dict=auth(**pyscript.app_config)
        
    url=f"https://api.switch-bot.com/v1.1/devices/{deviceId}/commands"
    myjson= {"command": command,"parameter": parameter,"commandType": commandType}
    requestHelper(url,myjson,headers_dict)

