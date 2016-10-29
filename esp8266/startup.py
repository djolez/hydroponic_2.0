from time import sleep
import logging
import ujson

import config
import mqtt_client
from ds18b20 import Ds18b20
from output_simple import OutputSimple

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def on_message(topic, msg):
    logger.debug('Topic {}, received msg: {}'.format(topic, msg))
    try:
        data = ujson.loads(msg)
        if(data['action'] is 'reregister'):
            register()
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
    devices['relay_3'] = OutputSimple(3)

devices = {}
client = None

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
        sleep(1)

main()
