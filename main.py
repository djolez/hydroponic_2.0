import logging
from time import sleep
import sys
import json

from module import *
from time_module import *
import helper

logging.basicConfig(level = logging.DEBUG, format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
logger = logging.getLogger(__name__)

def subscribe(client, userdata, flags, rc):
    logger.debug('Client connected')
    client.subscribe('main-dispatcher/#')
    client.message_callback_add('main-dispatcher/register', on_module_register)

def on_module_register(client, usrdata, msg):
    logger.debug('on_module_register -- {}'.format(msg.payload))
    try:
        data = json.loads(msg.payload.decode('utf-8'))
        name = data['module_name']
        if(name in modules):
            del modules[name]
        
        devices = data['devices'] if 'devices' in data else []
        modules[name] = Module(name, devices)

        #modules[name].devices[1].off()

        #a = Action('toggle', repeat=Time(second=3), callbacks=[toggle_relay])
        #a.schedule()
        
        modules['esp8266'].devices['float_switch_13'].interrupt_event.connect(toggle_relay)

    except ValueError:
        logger.error('Failed to parse payload as json')

state = 'off'
def toggle_relay(args=None):
    global state
    if(state is 'off'):
        modules['esp8266'].devices['relay_3'].on()
        state = 'on'
    else:
        modules['esp8266'].devices['relay_3'].off()
        state = 'off'

modules ={}

mqtt_client = helper.make_mqtt_client(subscribe, on_module_register)

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




