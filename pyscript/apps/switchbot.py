import time, hashlib, hmac, base64, requests
import re, yaml, io

PREFIX="switchbot_remote_"
DOMAIN="switch"
KEY_DEV_TYPE='remoteType'
KEY_DEV_NAME='deviceName'
KEY_DEV_ID='deviceId'
KEY_NON_IR_TYPE='deviceType'
KEY_NON_IR_CLOUD='enableCloudService'

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
  icons = {'Projector': 'projector', 'Light': 'lightbulb-on', 'TV':'television', 'Fan':'fan', 'Air Conditioner': 'air-conditioner'}
  typ = dev.get(KEY_DEV_TYPE)
  if typ in icons:
    ico = icons[typ]
  return 'mdi:'+ico

def gen_icon(non_ir):
  '''Generate icon based on device type. Default to a robot icon.'''
  ico = 'robot'
  icons = {'Curtain': 'curtains', 'Contact Sensor': 'leak', 'Meter': 'thermometer'}
  typ = non_ir.get(KEY_NON_IR_TYPE)
  if typ in icons:
    ico = icons[typ]
  return 'mdi:'+ico

def clear_existing():
  '''Clear switchbot devices which were saved to avoid zombies.'''
  states = state.names()
  for s in states:
    if PREFIX in s:
      log.warning(f"deleting sensor : {s}")
      state.delete(s)

def gen_dev_uid(dev:dict):
  '''Generate a Unique ID for Switchbot IR devices. (devices must have unique names in switchbot app so it works)'''
  name = dev.get(KEY_DEV_NAME)
  if name is not None:
    name = name.lower()
    name = re.sub(r'[^0-9a-z]+', '_', name)
    if name not in ['_', '']:
      return PREFIX+name
  return PREFIX + re.sub(r'[^0-9a-z]+', '_', str(dev.get(KEY_DEV_TYPE)).lower())+'_'+str(dev.get(KEY_DEV_ID)[-4:])

def gen_non_ir_uid(non_ir:dict):
  '''Generate a Unique ID for Switchbot non-IR devices. (devices must have unique names in switchbot app so it works)'''
  name = non_ir.get(KEY_DEV_NAME)
  domain = convert_switchbot_type_to_ha_domain(non_ir.get(KEY_NON_IR_TYPE))
  if name is not None:
    name = name.lower()
    name = re.sub(r'[^0-9a-z]+', '_', name)
    if name not in ['_', '']:
      return domain + '.' + PREFIX + name
  return domain + '.' + PREFIX + re.sub(r'[^0-9a-z]+', '_', str(non_ir.get(KEY_NON_IR_TYPE)).lower())+'_'+str(non_ir.get(KEY_DEV_ID)[-4:])

def convert_switchbot_type_to_ha_domain(type):
  if type == 'Curtain':
    return 'cover'
  elif type == 'Contact Sensor':
    return 'binary_sensor'
  elif type == 'Meter':
    return 'sensor'
  else:
    return 'switch'

def gen_dev_name(dev):
  name = ['Switchbot']
  if (dev.get(KEY_DEV_NAME) is not None):
    name.append(dev.get(KEY_DEV_NAME))
  #name.append(f"[IR {dev.get(KEY_DEV_TYPE)}]")
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

def create_ir_entities(devices):
  for dev in devices:
    log.warning(f"Adding Switchbot Device {dev.get(KEY_DEV_NAME)} [{dev.get(KEY_DEV_TYPE)}] -> {dev.get(KEY_DEV_ID)}")
    dev['friendly_name'] = gen_dev_name(dev)
    dev['icon'] = gen_icon(dev)
    state.set(f'{DOMAIN}.{gen_dev_uid(dev)}', value=dev.get(KEY_DEV_ID), new_attributes=dev )

def create_non_ir_entities(devices):
  for non_ir in devices:
    if non_ir.get(KEY_NON_IR_CLOUD): # Only load devices that are cloud-connected.
      log.warning(f"Adding Switchbot Device {non_ir.get(KEY_DEV_NAME)} [{non_ir.get(KEY_NON_IR_TYPE)}] -> {non_ir.get(KEY_DEV_ID)}")
      non_ir['friendly_name'] = gen_dev_name(non_ir)
      non_ir['icon'] = gen_icon(non_ir)
      state.set(f'{gen_non_ir_uid(non_ir)}', value=non_ir.get(KEY_DEV_ID), new_attributes=non_ir)
  switchbot_get_status() # Get an initial status for sensor-like devices.


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

def get_status(headers, device_id):
  url=f"https://api.switch-bot.com/v1.1/devices/{device_id}/status"
  r = requestGetHelper(url, {}, headers)
  data = r.json()
  status = data['statusCode']
  if status == 100:
    return data
  elif status == "n/a":
    log.warning(f"Status request for {device_id} unauthorized. Http 401 Error. User permission is denied due to invalid token.")
  elif status == 190:
    log.warning(f"Status request for {device_id}. System error. Device internal error due to device states not synchronized with server.")
  return None

#services
@service
@time_trigger("startup")
def switchbot_refresh_devices():
    """yaml
name: SwitchBot refresh devices
description: This service list registered devices in the "Switchbot Hubs". Devices are saved as "switch.switchbot_remote_<deviceName>" or similar in Home Assistant.
fields:
      """
    headers_dict=auth(**pyscript.app_config)
    url=f"https://api.switch-bot.com/v1.1/devices"
    r = requestGetHelper(url, {}, headers_dict)
    log.info(str(r.json()))
    infrared = r.json()['body'].get("infraredRemoteList")
    non_infrared = r.json()['body'].get("deviceList")
    if infrared and non_infrared is None:
      return None
    clear_existing()
    create_ir_entities(infrared)
    create_non_ir_entities(non_infrared)

@service
def switchbot_ir_hvac(device=None, temperature=None, mode=None, fan_speed=None, state=None):
    """yaml
name: SwitchBot IR HVAC Control
description: Control IR HVAC connected to your SwitchBot account.
fields:
  device:
    name: Device
    description: Target device
    example: switch.switchbot_remote_hvac
    default:
    required: true
    selector:
      entity:
        domain: switch

  state:
    name: Power State
    description: Select a State ("on" by Default)
    example: off
    default: on
    required: true
    selector:
      select:
        options:
          - on
          - off
        mode: list

  temperature:
    name: Temperature
    description: Select a target temperature (required for "on" state) (min 16 - Max 30) ("26" by Default)
    example: 26
    default: 26
    required: false
    selector:
      number:
        min: 16
        max: 30
        step: 1
        unit_of_measurement: "°C"
        mode: box

  mode:
    name: Mode
    description: Select a mode (required for "on" state) ("Auto" by Default)
    example: Auto
    default: Auto
    required: false
    selector:
      select:
        options:
          - Auto
          - Cool
          - Heat
          - Dry
          - Fan
        mode: list

  fan_speed:
    name: Fan Speed
    description: Select a Fan Speed (required for "on" state) ("Auto" by Default)
    example: Auto
    default: Auto
    required: false
    selector:
      select:
        options:
          - Auto
          - Low
          - Medium
          - High
        mode: list
      """
    deviceId = extract_device_id(device)
    headers_dict = auth(**pyscript.app_config)
    if temperature == None or state == "off":
      temperature = 26
    if mode == None or state == "off":
      mode = "Auto"
    if fan_speed == None or state == "off":
      fan_speed = "Auto"
    modes={"Auto": "1","Cool": "2","Dry": "3","Fan": "4","Heat": "5"}
    speeds={"Auto": "1","Low": "2","Medium": "3","High": "4"}
    command_execute(headers_dict, deviceId, 'setAll', parameter=f"{temperature},{modes[mode]},{speeds[fan_speed]},{state}")

@service
def switchbot_ir_light(device=None, command=None, steps=None):
    """yaml
name: SwitchBot IR Light Control
description: Control IR Light connected to your SwitchBot account.
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
    description: Select a Command
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
        mode: list
  steps:
    name: Steps
    description: Number of Steps (required for "brightnessUp" and "brightnessDown" command) ("1" by Default)
    example: 1
    default: 1
    required: false
    selector:
      number:
        min: 1
        max: 10
        mode: box
    """
    deviceId = extract_device_id(device)
    headers = auth(**pyscript.app_config)
    if steps == None or command == "turnOn" or command== "turnOff":
      steps=1
    for i in range(steps):
      command_execute(headers, deviceId, command)
    

@service
def switchbot_curtain(device=None, command=None, index=None, mode=None, position=None):
    """yaml
name: SwitchBot Curtain Command
description: Control Switchbot Curtain connected to your SwitchBot account.
fields:
  device:
    name: Device
    description: Target device
    example: cover.switchbot_remote_bedroom_curtains
    default:
    required: true
    selector:
      entity:
        domain: cover

  command:
    name: Command
    description: Select a Command
    example: turnOff
    default: 
    required: true
    selector:
      select:
        options:
          - turnOn
          - turnOff
          - setPosition
        mode: list

  index:
    name: Index [WIP]
    description: waiting for switchbot team clarifications ("0" by Default)
    example: 0
    default: 0
    required: false
    selector:
      number:
        min: 0
        max: 1
        step: 1
        mode: box

  mode:
    name: Mode
    description: Select a Mode (required for "setPosition" command) ("Default" by Default)
    example: Performance
    default: Default
    required: false
    selector:
      select:
        options:
          - Performance
          - Silent
          - Default 
        mode: list

  position:
    name: Position
    description: Select a Mode (0%-100%) (required for "setPosition" command) ("50" by Default)
    example: 50
    default: 50
    required: false
    selector:
      number:
        min: 0
        max: 100
        step: 1
        unit_of_measurement: "%"
        mode: box
    """
    
    deviceId = extract_device_id(device)
    headers_dict = auth(**pyscript.app_config)
    modes={"Performance": "0", "Silent": "1", "Default": "ff"}
    if position == None:
      position = "50"
    if index == None:
      index = "0"
    if command == "turnOn" or command == "turnOff":
      command_execute(headers_dict, deviceId, command, parameter=None)
    else:
      command_execute(headers_dict, deviceId, command, parameter=f"{index},{modes[mode]},{position}")

@service
def switchbot_bot(device=None, command=None, repetition=None):
    """yaml
name: SwitchBot Turn Device OFF
description: Turn Switchbot controlled device OFF
fields:
  device:
    name: Device
    description: Target device
    example: switch.switchbot_remote_bot
    default:
    required: true
    selector:
      entity:
        domain: switch
  command:
    name: Command
    description: Select a Command
    example: turnOff
    default: 
    required: true
    selector:
      select:
        options:
          - turnOn
          - turnOff
          - press
        mode: list
  repetition:
    name: Repetition
    description: Number of Repetition (required for "press" command) ("1" by Default)
    example: 1
    default: 1
    required: false
    selector:
      number:
        min: 1
        max: 10
        mode: box
    """
    deviceId = extract_device_id(device)
    headers_dict=auth(**pyscript.app_config)
    if repetition == None or not (command == "press"):
      repetition = 1
    for i in range(repetition): 
      command_execute(headers_dict, deviceId, command)

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
name: SwitchBot Generic Command
description: Control Switchbot Device through custom command(refer to https://github.com/OpenWonderLabs/SwitchBotAPI)
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
    description: The name of the command
    example: turnOff
    default: 
    required: true
    selector:
      text:

  parameter:
    name: Parameters
    description: Some commands require parameters, such as SetChannel
    example: 
    default: 
    required: false
    selector:
      text:

  commandType:
    name: Command Type
    description: For customized buttons, this needs to be set to customzie
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
    command_execute(headers_dict, deviceId, command, parameter=parameter, custom=(commandType=='customize'))

# Status checking
# Status requests got every 5 minutes (288 API calls / device / day).
#@time_trigger("period(0:00, 300 sec)")
def switchbot_get_status():
  states = state.names()
  for s in states:
    if (PREFIX in s):
      if KEY_NON_IR_TYPE in state.getattr(s).keys():
        deviceId = extract_device_id(s)
        headers_dict = auth(**pyscript.app_config)
        data = get_status(headers_dict, deviceId)
        if data != None:
          state.set(s, value=deviceId, new_attributes=data['body'])
