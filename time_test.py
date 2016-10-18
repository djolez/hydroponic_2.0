import logging
from time import sleep
import sys
import json

from device import *
from sensor import *
from module import *
import helper

logging.basicConfig(level = logging.DEBUG, format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
logger = logging.getLogger(__name__)

def subscribe(client, userdata, flags, rc):
    logger.debug('Client connected')
    client.subscribe('main-dispatcher/#')

def handle_msg(client, usrdata, msg):
    logger.debug('Client received message -- {}'.format(msg.payload))
    try:
        data = json.loads(msg.payload)
        if(data['action'] == 'module_on'):
            name = data['module_name']
            if(name in modules):
                del modules[name]
            
            sensors = data['sensors'] if 'sensors' in data else []
            devices = data['devices'] if 'devices' in data else []
            modules[name] = Module(name, sensors, devices)
    except ValueError:
        logger.error('Failed to parse payload as json')

modules ={}

mqtt_client = helper.make_mqtt_client(subscribe, handle_msg)

"""pump = Device('pump')
valve1 = Device('valve1')
float_switch_up = Device('float_switch_up')

float_switch_up.on_event.connect(pump.off)
float_switch_up.on_event.connect(valve1.off)

line1_on = [pump.on, valve1.on]
on = dt.datetime.now() + dt.timedelta(seconds=5)

all_actions = []
#all_actions.append(Action('line1_on', time=Time(on.hour, on.minute, on.second), callbacks=line1_on))

float_switch_up.on()

for a in all_actions:
    a.schedule()
"""

while True:
    try:
        sleep(0.1)
    except KeyboardInterrupt:
        logger.info('Exiting by user request')
        
        #for a in all_actions:
        #    a.deschedule()
        
        sys.exit(0)



