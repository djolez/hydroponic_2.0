import time
import logging
import ujson
import sys
import micropython
import gc

import config
import mqtt_client
from ds18b20 import Ds18b20
from output_simple import OutputSimple
from input_simple import InputSimple
import common

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def on_message(topic, msg):
    logger.debug('Topic {}, received msg: {}'.format(topic, msg))
    try:
        data = ujson.loads(msg)
        if(data['action'] is 'reregister'):
            register_module()
        elif(data['action'] is 'read'):
            devices[data['name']].read()
        elif(data['action'] is 'write'):
            devices[data['name']].write(data['value'])
    except ValueError:
        logger.error('Failed to parse msg: {}'.format(msg))
    except KeyError as e:
        logger.error('Message is missing field "{}"'.format(e))

def register_module():
    data = {}
    data['devices'] = []
    data['module_name'] = config.CONFIG['client_id']

    for name, device_object in devices.items():
        data['devices'].append({'name': name, 'device_type': device_object.device_type})

    client.publish('main-dispatcher/register', ujson.dumps(data))

def initialize_devices():
    add_device(Ds18b20(10))
    add_device(OutputSimple(15, name="relay", pwm_enabled=True))
    add_device(InputSimple(13, name='float_switch', trigger=InputSimple.trigger_type['any']))
    add_device(InputSimple(3, 'button', trigger=InputSimple.trigger_type['off']))

    d = add_device(InputSimple(0, name='poten', is_analog=True))
    register_analog(d.name)

def register_analog(name):
    global analog
    analog.append(name)

def read_analog():
    global analog, devices

    for device_name in analog:
        devices[device_name].update()

def add_device(d):
    global devices
    devices[d.name] = d
    return d

#devices that change state will update a variable from common as a flag
def check_device_changes():
    for name, device_object in common.state_changed.items():
        if(device_object is not None):
            device_object.interrupt()
            common.state_changed[name] = None

devices = {}
analog = []
client = None

def main():
    global client
    client = mqtt_client.make(config.CONFIG['client_id'])
    client.connect()
    client.set_callback(on_message)
    client.subscribe(config.CONFIG['client_id'])

    initialize_devices()
    register_module()

    while True:
        client.check_msg()
        read_analog()
        check_device_changes()

        #devices['poten_0'].read()
        time.sleep_ms(100)

main()
