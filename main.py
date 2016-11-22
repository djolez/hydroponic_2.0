import logging
from time import sleep
import sys
import json
import datetime

import helper
from classes.module import *

''' Everything is logged to a file '''
logging.basicConfig(
        level = logging.DEBUG,
        format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        filename='log/hydro.log')

''' Log INFO and higher to console  '''
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)

''' global vars '''
MODULES = {}

''' MQTT callbacks '''
def subscribe(client, userdata, flags, rc):
    logger.debug('Client connected')
    client.subscribe('main-dispatcher/#')
    client.message_callback_add('main-dispatcher/register', on_module_register)

def on_module_register(client, usrdata, msg):
    logger.debug('on_module_register -- {}'.format(msg.payload))
    try:
        global MODULES
        data = json.loads(msg.payload.decode('utf-8'))
        name = data['module_name']
        if(name in MODULES):
            del MODULES[name]
        
        devices = data['devices'] if 'devices' in data else []
        MODULES[name] = Module(name, devices)
    except ValueError:
        logger.error('Failed to parse payload as json')

''' /MQTT callbacks '''

mqtt_client = helper.make_mqtt_client(subscribe, on_module_register)

while True:
    try:
        sleep(0.1)
    except KeyboardInterrupt:
        logger.info('Exiting by user request')
        
        sys.exit(0)
