import time, hashlib, hmac, base64, requests
import re, yaml, io

PREFIX="switchbot_remote_"
DOMAIN="switch"
KEY_DEV_TYPE='remoteType'
KEY_DEV_NAME='deviceName'
KEY_DEV_ID='deviceId'

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

def gen_icon(dev):
  '''Generate icon based on device type. Default to a remote icon.'''
  ico = 'remote'
  icons = {'Projector': 'projector', 'Light': 'lightbulb-on', 'TV':'television', 'Fan':'fan'}
  typ = dev.get(KEY_DEV_TYPE)
  if typ in icons:
    ico = icons[typ]
  return 'mdi:'+ico

def clear_existing():
  '''Clear switchbot devices which were saved to avoid zombies.'''
  states = state.names(domain=DOMAIN)
  prefix = f'{DOMAIN}.{PREFIX}'
  for s in states:
    if s[0:len(prefix)] == prefix:
      log.warning(f"deleting sensor : {s}")
      state.delete(s)

def gen_dev_uid(dev:dict):
  '''Generate a Unique ID for Switchbot devices. (devices must have unique names in switchbot app so it works)'''
  name = dev.get(KEY_DEV_NAME)
  if name is not None:
    name = name.lower()
    name = re.sub(r'[^0-9a-z]+', '_', name)
    if name not in ['_', '']:
      return PREFIX+name
  return PREFIX + re.sub(r'[^0-9a-z]+', '_', str(dev.get(KEY_DEV_TYPE)).lower())+'_'+str(dev.get(KEY_DEV_ID)[-4:])


def gen_dev_name(dev):
  name = ['Switchbot']
  if (dev.get(KEY_DEV_NAME) is not None):
    name.append(dev.get(KEY_DEV_NAME))
  name.append(f"[IR {dev.get(KEY_DEV_TYPE)}]")
  return ' '.join(name)

def extract_device_id(device, _recursived=0):
  ''' Retrieve the Switchbot DeviceId. force refresh the devices list if the device doesnt exists.''' 
  try:
    uid = state.get(device)
    return uid
  except NameError:
    if _recursived == 0:
      switchbot_refresh_devices()
      return extract_device_id(device, _recursived=_recursived+1)
    else:
      msg=f'Warning: impossible to find {device}. [pyscript SwitchBot]'
      service.call('notify', 'persistent_notification', message=msg)
      #service.call('notify', 'notify', message=msg)
      return None



@pyscript_executor
def requestHelper(_url,_json,_headers):
    x=requests.post(_url,json = _json, headers=_headers)

@pyscript_executor
def requestGetHelper(_url,_json,_headers):
    return requests.get(_url,json = _json, headers=_headers)

def command_execute(headers, device_id, command, parameter=None, custom=False):
    url=f"https://api.switch-bot.com/v1.1/devices/{device_id}/commands"
    data= {"command": command, "commandType":"command"}
    if parameter is not None:
      data["parameter"] = parameter
    if custom:
      data["commandType"] = 'customize'
    requestHelper(url, data, headers)

#services
@service
def switchbot_refresh_devices():
    """yaml
name: SwitchBot refresh devices
description: This pyscript list registered devices in the "Switchbot Mini Hub". The devices are saved as "switch.switchbot_remote_<deviceName>" in Home Assistant and can be used for other commands.
fields:
      """
    headers_dict=auth(**pyscript.app_config)
    url=f"https://api.switch-bot.com/v1.1/devices"
    r = requestGetHelper(url, {}, headers_dict)
    log.info(str(r.json()))
    infrared = r.json()['body'].get("infraredRemoteList")
    if infrared is None:
      return None
    clear_existing()
    for dev in infrared:
        log.warning(f"Adding Switchbot Device {dev.get(KEY_DEV_NAME)} [{dev.get(KEY_DEV_TYPE)}] -> {dev.get(KEY_DEV_ID)}")
        dev['friendly_name'] = gen_dev_name(dev)
        dev['icon'] = gen_icon(dev)
        state.set(f'{DOMAIN}.{gen_dev_uid(dev)}', value=dev.get(KEY_DEV_ID), new_attributes=dev )

@service
def switchbot_hvac(device, temperature, mode, fan_speed, state):
    """yaml
name: SwitchBot HVAC API Interface
description: This (py)script allows you to control HVAC "saved" in "Switchbot Mini Hub" (or other switchbot brand ir blasters !! not yet tested !!).
fields:
  device:
    name: Device
    description: HVAC Target device
    example: switch.switchbot_remote_hvac
    default:
    required: true
    selector:
      entity:
        domain: switch

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
    deviceId = extract_device_id(device)
    headers_dict = auth(**pyscript.app_config)
    command_execute(headers_dict, deviceId, 'setAll', parameter=f"{temperature},{mode},{fan_speed},{state}")

@service
def switchbot_ir_light_control(device=None, command=None):
    """yaml
name: SwitchBot IR light control
description: Send command via infrared to light device.
fields:
  device:
    name: Device
    description: Target device
    example: switch.switchbot_remote_light
    default:
    required: true
    selector:
      entity:
        domain: switch
  command:
    name: Command
    description: the name of the command
    example: turnOff
    default: 
    required: true
    selector:
      select:
        options:
          - turnOn
          - turnOff
          - brightnessUp
          - brightnessDown
        mode: dropdown
    """
    device_id = extract_device_id(device)
    headers = auth(**pyscript.app_config)
    command_execute(headers, device_id, command)

@service
def switchbot_turn_on(device=None):

    """yaml
name: SwitchBot Turn Device ON
description: Turn Switchbot controlled device ON
fields:
  device:
    name: Device
    description: Target device
    example: switch.switchbot_remote_light
    default:
    required: true
    selector:
      entity:
        domain: switch
    """
    deviceId = extract_device_id(device)
    headers_dict = auth(**pyscript.app_config)
    command_execute(headers_dict, deviceId, "turnOn")

@service
def switchbot_turn_off(device=None):
    """yaml
name: SwitchBot Turn Device OFF
description: Turn Switchbot controlled device OFF
fields:
  device:
    name: Device
    description: Target device
    example: switch.switchbot_remote_light
    default:
    required: true
    selector:
      entity:
        domain: switch
    """
    deviceId = extract_device_id(device)
    headers_dict=auth(**pyscript.app_config)
    command_execute(headers_dict, deviceId, "turnOff")


@service
def switchbot_generic_command(device=None, command=None, parameter=None, commandType=None):
    """yaml
name: SwitchBot Generic Command API Interface
description: This (py)script allows you to control all device in your "Switchbot Home" (refer to https://github.com/OpenWonderLabs/SwitchBotAPI)
fields:
  device:
    name: Device
    description: Target device (get req. to api)
    example: switch.switchbot_remote_light
    default:
    required: true
    selector:
      entity:
        domain: switch

  command:
    name: Command
    description: the name of the command
    example: turnOff
    default: 
    required: true
    selector:
      text:

  parameter:
    name: Parameters
    description: some commands require parameters, such as SetChannel
    example: 
    default: 
    required: false
    selector:
      text:

  commandType:
    name: Command Type
    description: for customized buttons, this needs to be set to customzie
    example: command
    default: command
    required: true
    selector:
      select:
        options:
          - command
          - customize

      """
    deviceId = extract_device_id(device)
    headers_dict = auth(**pyscript.app_config)
    command_execute(headers_dict, deviceId, command, parameter=parameter, custom=(commandType=='custom'))