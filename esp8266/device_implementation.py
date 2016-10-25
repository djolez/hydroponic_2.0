import logging

from device import Device

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def handle_msg(msg):
    if(msg['action'] is 'change_state'):
        if(msg['state'] is None):
            logger.error('Missing device state')
            return
        devices[msg['name']].change_state(msg['state'])

devices = {}

devices['device_3'] = Device(3, 'out', 'device_3')
devices['device_15'] = Device(15, 'out', 'device_15')
