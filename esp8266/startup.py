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
import helper

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def on_message(topic, msg):
    logger.debug('Topic {}, received msg: {}'.format(topic, msg))
    try:
        data = ujson.loads(msg)
        if(data['action'] is 'reregister'):
            register()
        elif(data['action'] is 'add'):
            devices['relay_3'] = OutputSimple(3)
            print_mem()
        elif(data['action'] is 'remove'):
            del devices['relay_3']
            gc.mem_free()
            print_mem()
        elif(data['action'] is 'read'):
            devices[data['name']].read()
        elif(data['action'] is 'write'):
            devices[data['name']].write(data['value'])
    except ValueError:
        logger.error('Failed to parse msg: {}'.format(msg))
    except KeyError as e:
        logger.error('Message is missing field "{}"'.format(e))

def register():
    data = {}
    data['action'] = 'module_on'
    data['devices'] = []
    data['module_name'] = config.CONFIG['client_id']

    for name, device_object in devices.items():
        data['devices'].append({'name': name, 'device_type': device_object.device_type})

    client.publish('main-dispatcher', ujson.dumps(data))

def initialize_devices():
    global devices

    devices['ds18b20_10'] = Ds18b20(10)
    print_mem()
    
    #devices['relay_15'] = OutputSimple(15)
    #print_mem()

    #add_device(InputSimple(15, 'button', helper.trigger_type['on']))
    #add_device(InputSimple(0, 'poten', None, True))
    
    #import machine
    #a = machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING 
    add_device(InputSimple(13, 'float_switch', helper.trigger_type['any']))
    #add_device(InputSimple(13, 'float_switch', a))

devices = {}
client = None

def add_device(d):
    devices[d.name] = d

def print_mem():
    print('========================================')
    micropython.mem_info()
    print('========================================')

def check_device_changes():
    if(helper.state_changed is not ''):
        logger.debug('***CHANGED {}, value: {}'.format(helper.state_changed, devices[helper.state_changed].read()))
        helper.state_changed = ''


def main():
    global client
    client = mqtt_client.make(config.CONFIG['client_id'])
    #client = MQTTClient(config.CONFIG['client_id'], config.CONFIG['broker'])
    client.connect()
    client.set_callback(on_message)
    client.subscribe(config.CONFIG['client_id'])

    initialize_devices()
    register()

    while True:
        client.check_msg()
        check_device_changes()

        #devices['poten_0'].read()
        time.sleep_ms(100)

main()
